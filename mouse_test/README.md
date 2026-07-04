# Mouse Test Example

This example is the simplest way to confirm that USB HID works on your [Arduino® UNO Q](https://store.arduino.cc/products/uno-q). The script `mouse-test.py` moves the host computer's cursor in a small square using helper functions for moving, clicking, and scrolling.

## Hardware Setup

Connect the UNO Q to your host computer using a USB-C® cable. No extra hardware is required.

## Software Setup

This example has no external dependencies, so you can run it directly with the system Python — no virtual environment needed.

Copy this over to your board (either using `adb` or `ssh`):

```sh
adb push mouse_test /home/arduino
```

Then access the board and navigate into the mouse_test folder:

```sh
#access shell
adb shell

cd /home/arduino/mouse_test
```

Finally, run the script `mouse-test.py`:

```sh
python3 mouse-test.py
```

Your cursor should move in a small square.

> **Safety note:** This example moves your host computer's cursor. Stop the script with `Ctrl+C` to regain full control.
