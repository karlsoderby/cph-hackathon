<!--
SPDX-FileCopyrightText: Copyright (C) Arduino s.r.l. and/or its affiliated companies

SPDX-License-Identifier: MPL-2.0
-->

# HID Mouse over WebSocket

The **HID Mouse over WebSocket** example turns the [Arduino® UNO Q](https://store.arduino.cc/products/uno-q) into a WebSocket server that streams mouse-move HID reports. The board continuously generates a circular motion and broadcasts each step as a relative `(dx, dy)` report. A small receiver script running on your host computer connects to that socket and applies the moves to your real cursor, so the mouse drifts in circles.

Unlike the [Mouse Move](../mouse-move/) example, the board here does **not** act as a USB HID device. Instead it sends the HID data over the network, and any computer on the same link can subscribe to it.

## Bricks Used

**This example does not use any Bricks.** It runs a plain [`websockets`](https://websockets.readthedocs.io/) server inside the Python® layer of the App.

## Hardware and Software Requirements

### Hardware

- Arduino® UNO Q (x1)
- USB-C® cable (x1)

### Software

- Arduino App Lab (on the board)
- Python® 3.9+ (on the host computer)

## How to Use the Example

### 1. Run the app on the board

1. Connect the board to your host computer using USB-C®.
2. Open the App in Arduino App Lab and run it.
3. On start, the App opens a WebSocket server on port `8765` (`ws://0.0.0.0:8765`). App Lab installs the `websockets` dependency listed in [python/requirements.txt](python/requirements.txt) automatically.

> **Note:** The Python layer runs inside a container, so the port must be published to be reachable from your computer. This is done with the `ports:` entry in [app.yaml](app.yaml). If you change the port in `main.py`, update `app.yaml` to match and restart the App.

### 2. Find the board IP address

The host receiver needs the board's IP address on the USB/network link. You can find it in Arduino App Lab, or by opening a terminal on the board and running:

```bash
ip addr
```

Use the address the host computer can reach (for a USB link this is often something like `192.168.7.1`).

### 3. Run the receiver on your computer

From the `host/` folder:

```bash
python -m venv .venv
source .venv/bin/activate        # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
python receiver.py <board-ip>    # e.g. python receiver.py 192.168.7.1
```

Once connected, your mouse cursor starts moving in circles. Press `Ctrl+C` in the terminal to stop.

## Safety Notes

- This app moves your host computer cursor while the receiver is running.
- To stop control quickly, press `Ctrl+C` in the receiver terminal, or stop the App on the board.

## How it Works

- **Board side (`python/main.py`)** — On start, a background thread runs an `asyncio` WebSocket server. A motion loop walks around a circle and, on each tick (~33 Hz), computes the delta between the current and next point on the circle. That delta is broadcast to every connected receiver as a JSON HID report: `{"type": "mouse_move", "dx": <int>, "dy": <int>}`. Sending relative deltas mirrors how a real USB HID mouse reports movement.
- **Host side (`host/receiver.py`)** — The script connects to `ws://<board-ip>:8765`, reads each report, and calls `pynput`'s `mouse.move(dx, dy)` to move the local cursor. It automatically reconnects if the link drops.
