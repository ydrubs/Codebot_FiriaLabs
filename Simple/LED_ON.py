import serial
import time

def do_this():
    a = b"leds.user_num(1, True)\r\n"
    return a

# Replace with the correct port for your operating system
port = "COM4"  # For Linux/Mac, on Windows it could be 'COMx'
baudrate = 115200  # Default baudrate for CircuitPython

# Open serial connection
ser = serial.Serial(port, baudrate, timeout=1)

# Wait for the connection to stabilize
time.sleep(2)

# Send a command to the REPL (like help())
ser.write(b"help()\r\n")
ser.write(b"from botcore import *\r\n")
ser.write(b"leds.user_num(1, True)\r\n")

## Use a function to handle LED's
ser.write(do_this())

## LOOP Through and turn LED's off
while True:
    value = input("True or False: ")
    for i in range (4):
        t = f"leds.user_num({i}, {value})\r\n".encode()
        ser.write(t)

        response = ser.readline().decode('utf-8')
        if response:
            print(response)


# Read and print the response from the REPL (OPTIONAL)
while True:
    response = ser.readline().decode('utf-8')
    if response:
        print(response)

    # You can also send other commands to the REPL here:
    # ser.write(b"System.reboot()\r\n")

ser.close()