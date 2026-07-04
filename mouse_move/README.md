# Mouse Move Example

This example controls the mouse on your computer, using a Modulino Joystick.

## Hardware Setup

Connect the Modulino Joystick to the UNO Q via a Qwiic cable.

> You can replace the joystick with another modulino, but you will need to modify the existing code (both `mouse_move.py` and `mouse_move.ino`).

## Software Setup

To set it up, copy this over to your board (either using `adb` or `ssh`):

```sh
adb push mouse_move /home/arduino
```

Then access the board:

```sh
#access shell
adb shell

#install python venv
sudo apt install python3.12-venv

#install
python3 -m venv .venv
source .venv/bin/activate
```

Then we need navigate into the mouse_move folder, compile the Arduino sketch and upload it to the MCU:

```sh
cd /home/arduino/mouse_move
arduino-cli compile -b arduino:zephyr:unoq .
arduino-cli upload -b arduino:zephyr:unoq .
```

Finally, we can run the script `mouse_move.py`:

```sh
python3 mouse_move.py
```

