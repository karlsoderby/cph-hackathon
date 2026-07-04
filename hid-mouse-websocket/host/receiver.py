# SPDX-FileCopyrightText: Copyright (C) Arduino s.r.l. and/or its affiliated companies
#
# SPDX-License-Identifier: MPL-2.0

"""Host-side receiver for the "HID Mouse over WebSocket" UNO Q app.

Connects to the WebSocket server running on the board, receives relative
mouse-move HID reports, and applies them to the local cursor with pynput.

Usage:
    python receiver.py <board-ip>
    python receiver.py 192.168.7.1
    python receiver.py --port 8765 192.168.7.1
"""

import argparse
import asyncio
import json

import websockets
from pynput.mouse import Controller

mouse = Controller()

# Print at most one status line per this many reports to avoid flooding.
_LOG_EVERY = 30
_count = 0


def _apply_report(message: str):
    global _count
    data = json.loads(message)
    if data.get("type") == "mouse_move":
        dx = data.get("dx", 0)
        dy = data.get("dy", 0)
        before = mouse.position
        mouse.move(dx, dy)
        after = mouse.position

        _count += 1
        if _count % _LOG_EVERY == 1:
            moved = after != before
            hint = "" if moved else "  <-- cursor NOT moving (grant Accessibility permission)"
            print(f"report #{_count}: dx={dx:>3} dy={dy:>3} | pos {before} -> {after}{hint}")


async def run(uri: str):
    print(f"Connecting to {uri} ... (Ctrl+C to stop)")
    while True:
        try:
            async with websockets.connect(uri) as ws:
                print("Connected. Receiving mouse-move reports.")
                async for message in ws:
                    _apply_report(message)
        except (OSError, websockets.WebSocketException) as e:
            print(f"Connection lost ({e}). Retrying in 2 s ...")
            await asyncio.sleep(2)


def main():
    parser = argparse.ArgumentParser(description="Receive HID mouse moves from the UNO Q over WebSocket.")
    parser.add_argument("host", help="IP address or hostname of the UNO Q board")
    parser.add_argument("--port", type=int, default=8765, help="WebSocket server port (default: 8765)")
    args = parser.parse_args()

    uri = f"ws://{args.host}:{args.port}"
    try:
        asyncio.run(run(uri))
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
