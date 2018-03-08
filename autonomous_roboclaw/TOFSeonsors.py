import autonomous_roboclaw.VL53L0X as VL53L0X
import RPi.GPIO as GPIO
import time
from enum import Enum

class State(Enum):
    FREE = 0
    BLOCKED = 1
    ERROR = 2

class TOFSensor:
    tof_right = None
    tof_left = None
    sensor_right_shutdown = 0
    sensor_left_shutdown = 0
    state_left_sensor, state_right_sensor = State.FREE

    def __init__(self):
        # GPIO for Sensor 1 shutdown pin
        self.sensor_right_shutdown = 20
        # GPIO for Sensor 2 shutdown pin
        self.sensor_left_shutdown = 16

        GPIO.setwarnings(False)

        # Setup GPIO for shutdown pins on each VL53L0X
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.sensor_right_shutdown, GPIO.OUT)
        GPIO.setup(self.sensor_left_shutdown, GPIO.OUT)

        # Set all shutdown pins low to turn off each VL53L0X
        GPIO.output(self.sensor_right_shutdown, GPIO.LOW)
        GPIO.output(self.sensor_left_shutdown, GPIO.LOW)

        # Keep all low for 500 ms or so to make sure they reset
        time.sleep(0.50)

        # Create one object per VL53L0X passing the address to give to
        # each.
        self.tof_right = VL53L0X.VL53L0X(address=0x2B)
        self.tof_left = VL53L0X.VL53L0X(address=0x2D)

        # Set shutdown pin high for the first VL53L0X then
        # call to start ranging
        GPIO.output(self.sensor_right_shutdown, GPIO.HIGH)
        time.sleep(0.50)
        self.tof_right.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

        # Set shutdown pin high for the second VL53L0X then
        # call to start ranging
        GPIO.output(self.sensor_left_shutdown, GPIO.HIGH)
        time.sleep(0.50)
        self.tof_left.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
        # GPIO for Sensor 1 shutdown pin
        self.sensor_right_shutdown = 20
        # GPIO for Sensor 2 shutdown pin
        self.sensor_left_shutdown = 16

    def run(self):
        while True:
            if self.tof_right.get_distance() < 250:
                self.state_right_sensor = State.BLOCKED

            if self.tof_left.get_distance() < 250:
                self.state_left_sensor = State.BLOCKED

            if self.tof_right.get_distance() >= 250:
                self.state_right_sensor = State.FREE

            if self.tof_left.get_distance() >= 250:
                self.state_left_sensor = State.FREE

            time.sleep(0.05)
