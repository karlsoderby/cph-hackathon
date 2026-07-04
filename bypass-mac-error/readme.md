## Step 5 — Handle macOS Keyboard Setup Assistant

The first time macOS sees the keyboard it will show a **Keyboard Setup Assistant** dialog asking you to press the key to the right of the left Shift key. Run this to dismiss it:

```bash
python3 -c "
with open('/dev/hidg0','rb+') as h:
    h.write(bytes([0x00,0x64,0,0,0,0,0]))
    import time; time.sleep(0.05)
    h.write(bytes([0,0,0,0,0,0,0]))
print('done')
"
```