"""
PART OF THE FINAL!

This Pi will be receiving data so it will work as a server.
Server/store so it needs to run first to receive client.
"""

import time
import socket
import serial

# Setting up socket object & connection
command_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
command_server.bind(('', 5500))
command_server.listen(1)
print("Command server is listening & bound on port 5500...")
connection, address = command_server.accept()
print(f"Received connection from {address}")

# Setting up UART object & passing parameters
piCOM = serial.Serial(port='/dev/serial0', baudrate=115200)  # Change baud rate if needed
time.sleep(2)  # Give the serial connection time to settle

if piCOM.is_open:
    print("UART is open and ready")

cLOOP = ""  # Last valid command string

try:
    while True:
        mCombination = connection.recv(1024)  # Will be received in bytes
        if not mCombination:
            print("Data connection broken")
            break

        try:
            decoded = mCombination.decode("utf-8").strip()
        except UnicodeDecodeError:
            print("Bad data, not decoded")
            continue

        print(f"[TCP] Received: {decoded}")

        if decoded != cLOOP:
            cLOOP = decoded
            piCOM.write((decoded + "\n").encode())  
            print(f"[UART] Sent: {decoded}")

        time.sleep(0.1)

except Exception as e:
    print(f"Exception: {e}")

finally:
    connection.close()
    command_server.close()
    print("Sockets closed.")
