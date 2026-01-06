"""
Custom module I made that handles the stepper motor class definition

Make sure to save on Pico W 
"""
from machine import Pin
import time

class Motor:
    def __init__(self, pulse_pin, direction_pin):
        self.step_pin = Pin(pulse_pin, Pin.OUT)
        self.direction = Pin(direction_pin, Pin.OUT)
        self.delay_us = 200  # define delay as an instance variable

    def pulse(self):
        self.step_pin.value(1)
        time.sleep_us(self.delay_us)
        self.step_pin.value(0)
        time.sleep_us(self.delay_us)
        self.step_pin.value(1)
        time.sleep_us(self.delay_us)
        self.step_pin.value(0)
        time.sleep_us(self.delay_us)
        #print("Stepping", self.step_pin)

    # Direction control methods
    def right(self):
        self.direction.value(1)
        print("turning right")

    def left(self):
        self.direction.value(0)
        print("Turning left")

    def up(self):
        self.direction.value(1)
        print("turning up")

    def down(self):
        self.direction.value(0)
        print("turning down")
        