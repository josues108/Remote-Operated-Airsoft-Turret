"""
This python script will be handling ALL of the pico functions in the project

The Pico W automatically runs any code saved as "main.py" when powered up so make sure its uploaded as is.

I also made a custon module named "motors" which the script references. Make sure to save the motors module as well

This script will be handling the following:
- stepper motors' direction handling
- UART communication handling from PI
- BTS7960 airsoft/dc motor switching
"""
import machine
from machine import Pin, UART, PWM
import time
import math
import motors

# Set up UART1 on GP4 (TX) and GP5 (RX) at 115200 baud
pico_UART = UART(1, baudrate=115200, rx=Pin(5))

#Forward motion PWM object made
RPWM = PWM(Pin(10))
RPWM.freq(10000) #setting freq of 10Khz

LPWM = PWM(Pin(11))  # Use LPWM just to disable reverse
LPWM.freq(10000) #setting freq of 10Khz

#enable pin object
#Note on these enable pins, BOTH need to be high to work
REnable = Pin(12, Pin.OUT)
REnable.value(1) # this will enable forward motion

LEnable = Pin(13, Pin.OUT)
LEnable.value(1) # this will enable forward motion
#duty_u16() value controls speed (0 = off, 65535 = full speed).


#Cleaner object creation from our own built module
TOP = motors.Motor(20,21) #pulse,direction 
BOTTOM = motors.Motor(16,17)
    
def BR_TU(bottom,top):
        bottom.right()
        top.up()
        
def BR_TD(bottom,top):
        bottom.right()
        top.down()
        
def BL_TU(bottom,top):
        bottom.left()
        top.up()
        
def BL_TD(bottom,top):
        bottom.left()
        top.down()
        
def NA_TU(top):
        top.up()
        
def NA_TD(top):
        top.down()
        
def BR_NA(bottom):
        bottom.right()
        
def BL_NA(bottom):
        bottom.left()

def motor_ON():
    LPWM.duty_u16(0)    
    RPWM.duty_u16(65535)
    print("Fired")
    
def motor_OFF():
    LPWM.duty_u16(0)    
    RPWM.duty_u16(0)
    print("OFF")

motor_directions = { #need to research this lambda function
    "BR_TU": lambda: BR_TU(BOTTOM, TOP),
    "BR_TD": lambda: BR_TD(BOTTOM, TOP),
    "BL_TU": lambda: BL_TU(BOTTOM, TOP),
    "BL_TD": lambda: BL_TD(BOTTOM, TOP),
    
    "NA_TU": lambda: NA_TU(TOP),
    "NA_TD": lambda: NA_TD(TOP),
    "BL_NA": lambda: BL_NA(BOTTOM),
    "BR_NA": lambda: BR_NA(BOTTOM),
    }

#Helps set up while loop & LPWM constant to drive motor
last_command="NA_NA"
LPWM.duty_u16(0)

while True:
    #After first loop, last_command will have whatever the Pi sent last basically skipping the SLOW! UART read
    # Start of basic communication over UART
    if pico_UART.any():  # Checks for anything coming across. True when sees
        message = pico_UART.read(6)  # Reads up to 6 bytes
        #message=pico_UART.readline()
        if message:
            print("Raw UART:", repr(message))
            try:
                message=message.decode("utf-8").strip()
            except Exception as e:
                print("Messed up data:", message)
                continue
            
           
    #End of UART communication
            if message == "ONNNN":
                motor_ON()
            elif message == "OFFFF":
                motor_OFF()
                
            if message != last_command and message not in ("ONNNN", "OFFFF"):#if message=last command, skips to pulse function
                last_command=message
                action=motor_directions.get(message) #basically calls one of the functions from the lib
                if action:
                    action() #since the lib already has the built in directions, by calling this I set the direction functions
                    #print("New command:",message)

    if last_command != "NA_NA":
        if "BR" in last_command or "BL" in last_command: #calls .pulse(self) method to turn motor
            BOTTOM.pulse()
            #print("pulseB")
        if "TU" in last_command or "TD" in last_command: #calls .pulse(self) method to turn motor
            TOP.pulse()
            #print("pulseT")

    time.sleep_us(200)

