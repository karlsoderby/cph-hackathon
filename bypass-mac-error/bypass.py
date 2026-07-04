# Run this on the board will having the Mac keyboard wizard
with open('/dev/hidg0','rb+') as h:
    h.write(bytes([0x00,0x64,0,0,0,0,0]))
    import time; time.sleep(0.05)
    h.write(bytes([0,0,0,0,0,0,0]))
print('done')