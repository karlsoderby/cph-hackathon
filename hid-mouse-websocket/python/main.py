# SPDX-FileCopyrightText: Copyright (C) Arduino s.r.l. and/or its affiliated companies
#
# SPDX-License-Identifier: MPL-2.0

import asyncio
import json
import math
import threading

import websockets
from arduino.app_utils import App, Logger

logger = Logger("hid-mouse-websocket")

# Bind to every interface so the host computer can reach the server over the
# USB / network link. The host receiver connects to ws://<board-ip>:8765.
HOST = "0.0.0.0"
PORT = 8765

# Shape of the generated motion.
RADIUS = 120  # circle radius, in mouse pixels
ANGULAR_STEP = 0.12  # radians advanced per tick
TICK_SECONDS = 0.03  # ~33 reports per second

# Currently connected host receivers.
_clients = set()


async def _register(websocket):
    """Track a connected client until it disconnects."""
    _clients.add(websocket)
    logger.info(f"Receiver connected: {websocket.remote_address} ({len(_clients)} total)")
    try:
        await websocket.wait_closed()
    finally:
        _clients.discard(websocket)
        logger.info(f"Receiver disconnected ({len(_clients)} remaining)")


async def _motion_loop():
    """Walk around a circle and broadcast each step as a relative HID report."""
    angle = 0.0
    while True:
        next_angle = angle + ANGULAR_STEP
        # Send the delta between the current and next point on the circle so the
        # host moves the cursor relatively, exactly like a real HID mouse.
        dx = round(RADIUS * (math.cos(next_angle) - math.cos(angle)))
        dy = round(RADIUS * (math.sin(next_angle) - math.sin(angle)))
        angle = next_angle % (2 * math.pi)

        if _clients:
            report = json.dumps({"type": "mouse_move", "dx": dx, "dy": dy})
            websockets.broadcast(_clients, report)

        await asyncio.sleep(TICK_SECONDS)


async def _serve():
    async with websockets.serve(_register, HOST, PORT):
        logger.info(f"HID mouse WebSocket server listening on ws://{HOST}:{PORT}")
        await _motion_loop()


def _start_server():
    asyncio.run(_serve())


# Run the asyncio WebSocket server in a background thread so App.run() can keep
# the app alive on the main thread.
threading.Thread(target=_start_server, daemon=True).start()

App.run()
