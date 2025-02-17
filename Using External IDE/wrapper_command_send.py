import serial
import time

RIGHT = 1
LEFT = -1

class SerialCommandSender:
    def __init__(self, port="COM4", baudrate=115200):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)  # Allow time for the serial connection to stabilize

        # Ensure botcore is imported so commands work
        self.send_raw_command("help()")
        self.send_raw_command("from botcore import *")
        self.send_raw_command("from time import sleep")

        # Create namespaces for commands like leds and motors - Might need to have a dictionary for this as command set grows
        self.leds = SerialCommandNamespace(self, "leds")
        self.motors = SerialCommandNamespace(self, "motors")

    def sleep(self, duration):
        """Send a sleep command to the bot (bot handles the delay)."""
        command = f"sleep({duration})"  # Format the sleep command
        self.send_raw_command(command)  # Send the raw sleep command to the bot

    def send_raw_command(self, command):
        """Sends a raw string command to the serial port."""
        formatted_command = f"{command}\r\n"
        print(f"Sending: {formatted_command.strip()}")  # Debugging
        self.ser.write(formatted_command.encode())

    def __call__(self, *args, **kwargs):
        """Directly call methods on the bot instance."""
        return self.send_raw_command(*args, **kwargs)


class SerialCommandNamespace:
    def __init__(self, parent, prefix):
        self.parent = parent
        self.prefix = prefix

    def __getattr__(self, name):
        """Handles method calls for subcommands (like leds.user)."""
        return SerialCommandNamespace(self.parent, f"{self.prefix}.{name}")

    def __call__(self, *args):
        """When a command is called, format and send it."""
        # Convert arguments into a string format
        arg_str = ", ".join(repr(arg) for arg in args)
        # Build the full command and send it
        full_command = f"{self.prefix}({arg_str})"
        self.parent.send_raw_command(full_command)


# Initialize bot with `botcore` properly loaded
bot = SerialCommandSender()

# Assign namespaces globally for direct access
leds = bot.leds
motors = bot.motors
sleep = bot.sleep



# Example of usage without needing `bot.` prefix
if __name__ == "__main__":
    # # Initialize bot with `botcore` properly loaded
    # bot = SerialCommandSender()

    # # Assign namespaces globally for direct access
    # leds = bot.leds
    # motors = bot.motors
    # sleep = bot.sleep

    # Now you can use commands directly without `bot.` prefix
    leds.user(0b00000000)  # Turns off all LEDs
    sleep(0.5)  # Sleep command for the bot to handle
    leds.user(0b10101010)  # Turns on LEDs in a pattern

    # Example: Motor control
    motors.enable(True)  # Enable motors without `bot.`
    motors.run(RIGHT, -50)  # Run motor in the right direction at speed -50
    sleep(0.5)  # Wait for half a second
    motors.enable(False)  # Disable the motors to stop them

    # bot.leds.user_num(6,True)