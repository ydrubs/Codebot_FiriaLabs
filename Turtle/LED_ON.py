import turtle
import serial
import time
import threading

# Function to return the command string
def do_this():
    return b"leds.user_num(5, True)\r\n"

# Replace with the correct port for your operating system
port = "COM4"  # For Linux/Mac, on Windows it could be 'COMx'
baudrate = 115200  # Default baudrate for CircuitPython

# Open serial connection
ser = serial.Serial(port, baudrate, timeout=1)

# Wait for the connection to stabilize
time.sleep(2)
ser.write(b"from botcore import *\r\n")

# Variable to store the command string
command_string = b""

# Define the function to handle the click event
def on_button_click(x, y):
    global command_string
    # Check if the click is within the button's area
    if -60 < x < 60 and -20 < y < 20:
        command_string = do_this()
        print(f"Command stored: {command_string}")
        # Send the command to the serial connection
        ser.write(command_string)

# Define the serial communication thread
def serial_communication():
    while True:
        # Read and print the response from the REPL
        response = ser.readline().decode('utf-8')
        if response:
            print(response)

        # You can also send other commands to the REPL here:
        # ser.write(b"System.reboot()\r\n")

# Set up the turtle screen
screen = turtle.Screen()
screen.title("Turtle Button Example")
screen.bgcolor("white")

# Create a turtle to draw the button
button = turtle.Turtle()
button.shape("square")
button.color("blue")
button.shapesize(stretch_wid=2, stretch_len=6)  # Adjust size of the button
button.penup()
button.goto(0, 0)  # Position the button in the center

# Set up the click event listener
screen.onclick(on_button_click)

# Start the serial communication in a separate thread
serial_thread = threading.Thread(target=serial_communication, daemon=True)
serial_thread.start()

# Keep the screen open for turtle interaction
turtle.done()

# Close the serial connection after use
ser.close()
