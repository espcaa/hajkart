import time
import board
import digitalio
import pwmio
from adafruit_motor import servo
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

# --- BLE Setup ---
ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

# --- Tail Servo ---
tail_pwm = pwmio.PWMOut(board.P0_02, duty_cycle=2 ** 15, frequency=50)
tail_servo = servo.Servo(tail_pwm)

def wag_tail():
    for _ in range(3):
        tail_servo.angle = 180
        time.sleep(0.3)
        tail_servo.angle = 0
        time.sleep(0.3)
    tail_servo.angle = 90

# --- Motor Pins ---
LEFT_STEP_PIN = board.P0_22
LEFT_DIR_PIN = board.P0_20
RIGHT_STEP_PIN = board.P0_31
RIGHT_DIR_PIN = board.P0_29

left_step = digitalio.DigitalInOut(LEFT_STEP_PIN)
left_step.direction = digitalio.Direction.OUTPUT
left_dir = digitalio.DigitalInOut(LEFT_DIR_PIN)
left_dir.direction = digitalio.Direction.OUTPUT

right_step = digitalio.DigitalInOut(RIGHT_STEP_PIN)
right_step.direction = digitalio.Direction.OUTPUT
right_dir = digitalio.DigitalInOut(RIGHT_DIR_PIN)
right_dir.direction = digitalio.Direction.OUTPUT

def set_motor_directions(left_forward, right_forward):
    left_dir.value = left_forward
    right_dir.value = not right_forward  # right is inverted

def step_motors(steps, left_on=True, right_on=True):
    for _ in range(steps):
        if left_on:
            left_step.value = True
        if right_on:
            right_step.value = True
        time.sleep(0.0006)
        left_step.value = False
        right_step.value = False
        time.sleep(0.0006)

def move(key):
    if key == "w":
        print("Forward")
        set_motor_directions(True, True)
        step_motors(1000)
    elif key == "s":
        print("Backward")
        set_motor_directions(False, False)
        step_motors(1000)
    elif key == "a":
        print("Left")
        set_motor_directions(True, True)
        step_motors(1000, left_on=False, right_on=True)
    elif key == "d":
        print("Right")
        set_motor_directions(True, True)
        step_motors(1000, left_on=True, right_on=False)
    elif key == "t":
        print("Wag")
        wag_tail()
    else:
        print("Unknown:", key)

# --- BLE Loop ---
print("Starting BLE...")

while True:
    if not ble.connected:
        if not ble.advertising:
            ble.start_advertising(advertisement)
            print("Advertising...")
        time.sleep(0.1)
        continue

    if ble.advertising:
        ble.stop_advertising()
    print("Connected!")

    while ble.connected:
        if uart.in_waiting:
            raw = uart.read(1)
            if raw:
                try:
                    key = raw.decode("utf-8").lower()
                    print("Received:", key)
                    move(key)
                except:
                    pass
        time.sleep(0.01)

    print("Disconnected!")
