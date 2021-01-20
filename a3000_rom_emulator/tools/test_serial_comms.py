import random

from arcflash import uploader

def main():
    print("Programming 16MB of random data into Arcflash to see if we can crash the serial port")

    SIZE = 16*1024*1024
    # Python 3.9 lets us do this, but Ubuntu doesn't have 3.9 yet: rom = random.randbytes(SIZE)
    rom = random.Random().getrandbits(SIZE * 8).to_bytes(SIZE, 'little')
    uploader.upload(rom)

if __name__ == '__main__':
    main()
