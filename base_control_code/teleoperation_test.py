from gpiozero import Robot, Motor
from pynput import keyboard
from time import sleep

# define motors of Robot - GPIO pins 7,8 for motor 1, and 10,9 for motor 2
# we did 10,9 instead of 9,10 because of how the motor is wired to the motor controller
rover = Robot(left = (7,8), right = (10, 9))

try:
    while True:

        def on_press(key):
            if key.char == 'w':
                rover.forward(0.8)
            elif key.char == 's':
                rover.backward(0.8)
            elif key.char == 'a':
                rover.left()
            elif key.char == 'd':
                rover.right()
            # catch error message for when non-WASD character is accidentally pressed
            else:
                pass
        
        # stop rover on button release - don't want it to still move when letting go of WASD
        def on_release(key):
            rover.stop()
        
        # connect on_press and on_release functions to pynput.keyboard.Listener class
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
# stop rover on Ctrl+C
except KeyboardInterrupt:
    rover.stop()
