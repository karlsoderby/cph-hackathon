# HID on the Arduino UNO Q

This repository collects examples for using **USB HID (Human Interface Device)** on the [Arduino® UNO Q](https://store.arduino.cc/products/uno-q). The UNO Q can act as a USB mouse or keyboard toward a host computer, letting you move the cursor, click, scroll, and type directly from code running on the board's Linux side.

The examples range from a minimal "hello world" mouse mover to a joystick-controlled cursor, a keyboard typer, and a networked WebSocket variant.

## What is HID here?

On the UNO Q, the Linux system exposes USB HID gadget devices: a mouse at `/dev/hidg1` and a keyboard at `/dev/hidg0`. Writing a small report to one of these devices sends an event to the connected host. For the mouse:

```python
def mouse_report(buttons=0, x=0, y=0, scroll=0):
    with open('/dev/hidg1', 'rb+') as hid:
        hid.write(bytes([buttons, x & 0xff, y & 0xff, scroll & 0xff]))
```

The mouse report is 4 bytes: button state, relative X, relative Y, and scroll. The keyboard uses a similar approach, writing key reports to `/dev/hidg0`. This is the foundation used across all the examples in this repo.

## Examples

### [`mouse_test/`](mouse_test/README.md)

The simplest starting point. A standalone script with helper functions for moving, clicking, and scrolling the mouse. Running it draws a small square with the cursor. Use this to confirm HID works on your board. See the [example README](mouse_test/README.md) for setup and run instructions.

### [`keyboard_test/`](keyboard_test/README.md)

A standalone script that types a string of text into the focused window on the host computer. Running it types `Hello, World!` after a short countdown. Use this to confirm HID keyboard input works on your board. See the [example README](keyboard_test/README.md) for setup and run instructions.

### [`mouse_move/`](mouse_move/README.md)

Controls the host computer's mouse using a **Modulino® Joystick** connected over Qwiic. An Arduino sketch (`mouse_move.ino`) reads the joystick on the microcontroller and forwards movement to the Linux side, where `mouse_move.py` turns it into HID reports. See the [example README](mouse_move/README.md) for setup and upload instructions.

### [`hid-mouse-websocket/`](hid-mouse-websocket/README.md)

An [Arduino App Lab](https://docs.arduino.cc/software/app-lab/) App where the UNO Q does **not** act as a USB HID device. Instead it runs a WebSocket server that broadcasts mouse-move reports over the network. A receiver script on your host computer applies the moves to the real cursor. See the [example README](hid-mouse-websocket/README.md) for details.

## Requirements

- Arduino® UNO Q (x1)
- USB-C® cable (x1)
- For `mouse_move`: a Modulino® Joystick and a Qwiic cable
- Python® 3 on the board (and, for the WebSocket example, on the host computer)

## Getting Started

1. Connect the UNO Q to your computer with a USB-C® cable.
2. Access the board over `adb` or `ssh`.
3. Copy an example onto the board, for example:

   ```sh
   adb push mouse_test /home/arduino
   ```

4. Run the script on the board:

   ```sh
   adb shell
   cd /home/arduino/mouse_test
   python3 mouse-test.py
   ```

The cursor on your host computer should start moving.

> **Safety note:** These examples move your host computer's cursor. Stop the script (`Ctrl+C`) or the App to regain full control.
