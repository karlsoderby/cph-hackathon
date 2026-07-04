# Keyboard Test Example

This example is the simplest way to confirm that USB HID keyboard input works on your [Arduino® UNO Q](https://store.arduino.cc/products/uno-q). The script `keyboard.py` types a string of text into whatever text field is focused on the host computer.

## Hardware Setup

Connect the UNO Q to your host computer using a USB-C® cable. No extra hardware is required.

## Software Setup

This example has no external dependencies, so you can run it directly with the system Python — no virtual environment needed.

Copy this over to your board (either using `adb` or `ssh`):

```sh
adb push keyboard_test /home/arduino
```

Then access the board and navigate into the keyboard_test folder:

```sh
#access shell
adb shell

cd /home/arduino/keyboard_test
```

Finally, run the script `keyboard.py`:

```sh
python3 keyboard.py
```

The script waits 5 seconds before typing, so switch to a text editor or text field on your host computer. It then types `Hello, World!`.

> **Safety note:** This example sends keystrokes to your host computer. Make sure the focused window is a safe place to type before the 5-second countdown ends.
