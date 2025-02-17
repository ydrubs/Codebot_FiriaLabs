"""
Copy this code into main.py in order to run code locally.
This allows programming outside of Codespace
"""

from wrapper_command_send import *


# Now you can use commands directly without `bot.` prefix
leds.user(0b00000000)  # Turns off all LEDs
sleep(0.5)  # Sleep command for the bot to handle
leds.user(0b10101010)  # Turns on LEDs in a pattern

# Example: Motor control
motors.enable(True)  # Enable motors without `bot.`
motors.run(RIGHT, -50)  # Run motor in the right direction at speed -50
sleep(0.5)  # Wait for half a second
motors.enable(False)  # Disable the motors to stop them

bot.leds.user_num(6,True) # We can alos use the bot namespace if we did not define it globally (inside of wrapper_command_send)