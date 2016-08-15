#!/usr/bin/env python

"""Main file to run the Rotacaster demo bot."""

from pwm import Pwm
import pygame
from pygame.locals import *
from commands import *
#from bno055 import BNO055
import os, time

MOTOR_A_PWM = "PWM0B-29"
MOTOR_B_PWM = "PWM1A-36"
MOTOR_C_PWM = "PWM2A-45"

CANCEL_COMMAND_DEAD_ZONE = 0.3
DISABLE_THRESH = 0.1
DISABLE_TIME = 10

axis_map = {"left_stick_x" : 0, "left_stick_y" : 1, "right_stick_x" : 2, "right_stick_y" : 3,
            "left_trigger" : 4, "right_trigger" : 5}

button_map = {"a" : 0, "b" : 1, "x" : 2, "y" : 3, "left_button" : 4, "right_button" : 5, "back" : 6, "start" : 7, "left_stick_press" : 9, "right_stick_press" : 10}

loop_speed = 1/50.0 #loop speed, seconds

class DummyGyro(object):
    def get_yaw(self):
        return 0.0

def main():
    pid = str(os.getpid())
    file("/var/run/rotacaster.pid", "w").write(pid)

    pwm_a = Pwm(MOTOR_A_PWM)
    pwm_b = Pwm(MOTOR_B_PWM)
    pwm_c = Pwm(MOTOR_C_PWM)
    pwms = [pwm_a, pwm_b, pwm_c]
    for p in pwms:
        p.pwm_off()
    # TODO: replace with real bno class
    gyro = DummyGyro()

    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()
    js = pygame.joystick.Joystick(0)
    js.init()
    axis = [0.0 for x in range(len(axis_map))]
    last_input = time.time()
    rotation_locker = 0.0

    command = None
    last_loop = time.time()

    while True:
        #wait until we want to start next loop
        while time.time()-last_loop<loop_speed:
            pass

        active_buttons = [False for x in range(len(button_map))]
        for event in pygame.event.get():
                if event.type == JOYAXISMOTION:
                    if event.axis < len(axis_map):
                        axis[event.axis] = event.value
                elif event.type == JOYBUTTONDOWN and event.button < len(button_map):
                    active_buttons[event.button] = True

        # first check for enabling
        if (active_buttons[button_map["left_button"]]
            and active_buttons[button_map["right_button"]]):
            command = drive
            for p in pwms:
                p.pwm_on()

        # disable if we haven't moved the sticks in a while
        if (axis[axis_map["left_trigger"]] > DISABLE_THRESH
            or axis[axis_map["right_trigger"]] > DISABLE_THRESH
            or (time.time() - last_input > DISABLE_TIME 
                and command is drive):
            command = None
            for p in pwms:
                p.pwm_off()
        
        if not command:
            continue
        
        # if we are moving the sticks
        if True in map(lambda x: abs(x)>CANCEL_COMMAND_DEAD_ZONE, axis_map):
            command = drive

        if True in map(lambda x: abs(x)>0.05, axis_map) or True in button_map:
            last_input = time.time()

        if active_buttons[button_map["right_stick_press"]]:
            if rotation_locker:
                rotation_locker = 0.0
            else:
                rotation_locker = axis[axis_map["right_stick_x"]]



        if active_buttons[button_map["a"]] and command is drive:
            command = square
        if active_buttons[button_map["b"]] and command is drive:
            command = circle
        
        # Run the particular command that is set
        if command is drive:
            command = command(
                        axis[axis_map["left_stick_y"]],
                        axis[axis_map["left_stick_x"]],
                        rotation_locker if rotation_locker else axis[axis_map["right_stick_x"]],
                        1.0, gyro, pwms
                    )
        else
            command = command(gyro, pwms)




if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print e
        pa = Pwm(MOTOR_A_PWM)
        pb = Pwm(MOTOR_B_PWM)
        pc = Pwm(MOTOR_C_PWM)
        pa.set_speed(0.0)
        pb.set_speed(0.0)
        pc.set_speed(0.0)
        print "Exception Thrown, all motors stopped"
