import os
import sys

import serial.tools.list_ports

assert sys.version_info[0] >= 3, "Python 3+ required"

here = os.getcwd()
build_path = os.path.join(
    here,
    "build_output_%s" % sys.platform,  # just in case things differ between platforms
)

arduino_cli = "arduino-cli"  # in case we need a path to it at some point
std_args = "--verbose --fqbn arduino:samd:adafruit_circuitplayground_m0"

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

os.system("%s compile %s --libraries src --build-path %s" % (
    arduino_cli,
    std_args,
    build_path,
))

os.system("%s upload %s --port %s --input-dir %s" % (
    arduino_cli,
    std_args,
    upload_port,
    build_path,
))
