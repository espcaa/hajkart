import asyncio
from bleak import BleakClient, BleakScanner
import sys
import tty
import termios

# Nordic UART Service UUIDs
UART_SERVICE_UUID = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
UART_TX_CHAR_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"  # Write to peripheral

DEVICE_NAME = "CIRCUITPY7424"

# Read one char at a time (Unix)
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

async def run():
    print(f"Scanning for device named '{DEVICE_NAME}'...")
    device = None
    devices = await BleakScanner.discover(timeout=5.0)
    for d in devices:
        if d.name == DEVICE_NAME:
            device = d
            break
    if not device:
        print("Device not found. Exiting.")
        return

    print(f"Found device: {device.address}. Connecting...")
    async with BleakClient(device) as client:
        if not client.is_connected:
            print("Failed to connect.")
            return
        print("Connected! Type commands (w/a/s/d/t), 'q' to quit.")

        while True:
            ch = getch()
            if ch == "q":
                print("\nQuitting.")
                break
            try:
                await client.write_gatt_char(UART_TX_CHAR_UUID, ch.encode('utf-8'))
                print(f"Sent: {ch}")
            except Exception as e:
                print(f"Failed to send: {e}")
                break

asyncio.run(run())
