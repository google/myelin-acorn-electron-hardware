import os
import sys

import serial.tools.list_ports

assert sys.version_info[0] >= 3, "Python 3+ required"

def cmd(s):
    print(s)
    return os.system(s)

here = os.getcwd()
build_path = os.path.join(
    here,
    "build_output_%s" % sys.platform,  # just in case things differ between platforms
)

# Allow overriding arduino-cli with a local version
arduino_cli = os.environ.get("ARDUINO_CLI", "arduino-cli")

# std_args = "--verbose --fqbn arduino:samd:adafruit_circuitplayground_m0"
std_args = "--verbose --fqbn myelin:samd:arcflash --config-file ./arduino-cli.json"

# Figure out where the Arcflash is plugged in
upload_port = None
for port in serial.tools.list_ports.comports():
    print(port.device,
        port.product,
        port.hwid,
        port.vid,
        port.pid,
        port.manufacturer,  # "Adafruit"
    )
    if port.vid == 0x1209 and port.pid == 0xFE07:
        print("Found an Arcflash at %s" % port.device)
        upload_port = port.device
    elif port.vid == 0x239A and port.pid in (0x0018, 0x8018):
        print("Found a Circuit Playground Express at %s" % port.device)
        upload_port = port.device

if "ARCFLASH_PORT" in os.environ:
    upload_port = os.environ["ARCFLASH_PORT"]
    print("Using %s from ARCFLASH_PORT environment variable" % upload_port)

if not upload_port:
    raise Exception("Could not find a connected Arcflash")

print("Using %s as the upload port" % upload_port)

# Copy xsvftool if necessary
xsvf_path = "../../third_party/libxsvf"
xsvf_dest = "src/libxsvf"
os.makedirs(xsvf_dest, exist_ok=True)
for f in os.listdir(xsvf_path):
    if os.path.splitext(f)[1] not in (".c", ".cpp", ".h"): continue
    if f in ("xsvftool-ft232h.c", "xsvftool-gpio.c"): continue
    src = os.path.join(xsvf_path, f)
    dest = os.path.join(xsvf_dest, f)

    content = open(src).read()
    if not os.path.exists(dest) or open(dest).read() != content:
        open(dest, "w").write(content)
        print("  %s -> %s" % (src, dest))

# Build it
cmd("%s compile %s --libraries src --build-path %s" % (
    arduino_cli,
    std_args,
    build_path,
))

# And upload to the Arcflash board
cmd("%s upload %s --port %s --input-dir %s" % (
    arduino_cli,
    std_args,
    upload_port,
    build_path,
))

print("\n"
      "Done!  If you get a popup about ARCBOOT not being ejected properly, ignore it;\n"
      "it's a side effect of the UF2 bootloader resetting after the download.")