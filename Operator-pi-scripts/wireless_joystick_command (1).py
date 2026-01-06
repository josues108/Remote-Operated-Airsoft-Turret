'''
PART OF THE FINAL

This code will be for sending commands over TCP. It will read the joystick values then send it over the socket.
The operator Pi will be the client in this case as it initiates the connection

client NEEDS Server/store open first
'''
import socket
import time
import spidev
from gpiozero import Button #doc says it should be explicitly imported
from signal import pause



#spi setup for ADC control
spi = spidev.SpiDev()
spi.open(0,0) #openspi CE0
spi.max_speed_hz = 1350000

def read_channel(ch):
    adc = spi.xfer2([1, (8+ch) << 4, 0])
    return ((adc[1] & 3) << 8) | adc[2]

#functions for button interrupt
def button_ONhandler():
    commander_client.sendall(b"ONNNN\n") #ill most likely test this tomorrow with a better send
    print("Button Pressed")
    
def button_OFFhandler():
    commander_client.sendall(b"OFFFF\n")    #need to edit this MAYBE and need to put something on the receiver
    print("Button off")
    
# Setting up TCP server & socket object creation
commander_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Change this to your local Pi IP
commander_client.connect(("X.X.X.X",5500)) 
#  changing IP to be into EDUROAM

#button interrupt set up
button = Button(2) # this lib uses the BCM numbering not physical, gpio 2
button.when_pressed = button_ONhandler #from doc, it does not run function but creates a reference to the function
button.when_released = button_OFFhandler


# Loop to send message repeatedly
bottom="NA"
top="NA"
cLOOP="start"
while True:
    #Start of ADC reading
    x = read_channel(1) #VRx on Ch0
    y = read_channel(2) #Vry on Ch1
    print(f"X: {x}, Y: {y}")
    
    #start of UART Message sending
    if x>990:
        bottom="BR"
    elif x<100:
        bottom = "BL"
    else:
        bottom="NA"
    
    if y>900:
        top= "TD"
    elif y<100:
        top="TU"
    else:
        top="NA"
        
    combination= f"{bottom}_{top}"       #want to research this more:byte encoding
#     print(combination)
    if combination != cLOOP: #If combination =cLOOP, so basically no change in action then it doesnt send a UART
        cLOOP=combination
        #add TCP command sending here
        dataTrans = (combination + "\n").encode()
        print("Data sent is: ",dataTrans)
        commander_client.sendall(dataTrans)
    
    
    time.sleep(.5)  # Wait 1 second before sending again

commander_client.close()
