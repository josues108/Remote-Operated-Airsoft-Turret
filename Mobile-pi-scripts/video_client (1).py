"""
PART OF THE FINAL!

This mobile pi is the client and innitiates the video stream
"""


import cv2
from picamera2 import Picamera2
import socket
import struct


#picam object creation & basic set up
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480) #sets up parameters of video
picam2.preview_configuration.main.format = "RGB888" #in RGB space
picam2.configure("preview")
picam2.start()

#socket object creation
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Make sure to change this to your operator PI IP
client.connect(("X.X.X.X", 5000))  # IP of operator Pi

while True:
    frame = picam2.capture_array() #caputuring a single camera frame from the pi camera2 object
    _, img_encoded = cv2.imencode(".jpg", frame) 
    data = img_encoded.tobytes() #converts encoded image to raw bytes object
    client.sendall(struct.pack(">L", len(data)) + data)
