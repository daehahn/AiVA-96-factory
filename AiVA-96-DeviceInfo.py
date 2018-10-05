import usb.core
import usb.util

VID = 0x20B1
PID = 0x0011

dev = usb.core.find(idVendor=VID, idProduct=PID)
if dev is None:
        print("Cound not find AiVA device :(")
        exit(1)
print("Yeeha! Found a AiVA device")

print("Firmware version: " + hex(dev.bcdDevice))
print("Serial number: " + usb.util.get_string(dev, dev.iSerialNumber))