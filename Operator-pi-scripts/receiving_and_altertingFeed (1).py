'''
PART OF THE FINAL!!

So in this case the operator pi is the server as it is listening in to video connections

'''


import socket
import struct
import numpy as np
import cv2
import time

# Setting up TCP server & socket object creation
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 5000))  # Listen on all interfaces, port 5000
server_socket.listen(1)
print("[INFO] Waiting for connection...")

connection, address = server_socket.accept()
print(f"[INFO] Connected to {address}")
fps=0
# Receive loop
while True:
    tStart=time.time()
    # Receive the 4-byte length prefix
    raw_size = connection.recv(4)
    
    #checking if socket sending in empty t/f
    if not raw_size:
        print("Connection closed by sender.")
        break

    frame_size = struct.unpack(">L", raw_size)[0]

    # Receiving the full JPEG frame
    #Magic and byte data happens here
    data = b''
    while len(data) < frame_size:
        packet = connection.recv(frame_size - len(data))
        if not packet:
            break
        data += packet

    # Decoding display
    frame = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), cv2.IMREAD_COLOR)
    
    #adding text and bullseye
    text="FPS:"+ str(int(fps))
    cv2.putText(frame,text,(30,60),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
    #cv2.circle(frame,center,r,cColor,cThick)
    cv2.circle(frame,(320,240),20,(0,0,255),3)
    cv2.circle(frame,(320,240),2,(0,0,255),2)
    cv2.imshow("Live Feed", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("[INFO] Exiting viewer.")
        break
    
    #FPS math
    tEnd=time.time()
    loopTime=tEnd-tStart
    fps=.9*fps + .1*(1/loopTime)
    
    
connection.close()
cv2.destroyAllWindows()
