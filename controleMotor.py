#!/usr/bin/env python
# coding: latin-1
# Autor:    Ingmar Stapel
# Datum:    20160731
# Version:    2.0
# Homepage:    http://custom-build-robots.com

from time import sleep
import RPi.GPIO as io

io.setmode(io.BCM)

io.setwarnings(False)

L_L_EN = 17 # L_L_EN
io.setup(L_L_EN, io.OUT)
io.output(L_L_EN, True)

L_R_EN = 18 # L_R_EN
io.setup(L_R_EN, io.OUT)
io.output(L_R_EN, True)

R_L_EN = 6 # R_L_EN
io.setup(R_L_EN, io.OUT)
io.output(R_L_EN, True)

R_R_EN = 12 # R_R_EN
io.setup(R_R_EN, io.OUT)
io.output(R_R_EN, True)

L_L_PWM = 22 # leftmotorpwm_pin_l
L_R_PWM = 23 # leftmotorpwm_pin_r

io.setup(L_L_PWM, io.OUT)
io.setup(L_R_PWM, io.OUT)
leftmotorpwm_l = io.PWM(L_L_PWM, 100)
leftmotorpwm_r = io.PWM(L_R_PWM, 100)
leftmotorpwm_l.start(0)
leftmotorpwm_r.start(0)
leftmotorpwm_l.ChangeDutyCycle(0)
leftmotorpwm_r.ChangeDutyCycle(0)

R_L_PWM = 13 # rightmotorpwm_pin_l
R_R_PWM = 19 # rightmotorpwm_pin_r

io.setup(R_L_PWM, io.OUT)
io.setup(R_R_PWM, io.OUT)
rightmotorpwm_l = io.PWM(R_L_PWM, 100)
rightmotorpwm_r = io.PWM(R_R_PWM, 100)
rightmotorpwm_l.start(0)
rightmotorpwm_r.start(0)
rightmotorpwm_l.ChangeDutyCycle(0)
rightmotorpwm_r.ChangeDutyCycle(0)

def setMotor(power_l, power_r):
    leftmotorpwm_r.ChangeDutyCycle(power_r)
    leftmotorpwm_l.ChangeDutyCycle(power_l)

def exit():
    io.output(L_L_EN, False)
    io.output(L_R_EN, False)
    io.output(R_L_EN, False)
    io.output(R_R_EN, False)
    io.cleanup()

PWM_MAX = 75
PWM_MIN = -25
CHANGE_VALUE = 1

def controleStart(queueKey=None, flag=None, quit=None):
    print("Starting motor")

    vel_l = vel_r = 0
    key = lastkey = "none"

    while not quit.is_set():
        sleep(.25)

        if not flag.is_set() or flag is None:
            try:
                key = queueKey.get_nowait()
                print(f"Getting {key} key")
            except:
                key = "none"

            if key == "up":
                vel_l += CHANGE_VALUE * 10
                vel_r += CHANGE_VALUE * 10
            elif key == "down":
                vel_l -= CHANGE_VALUE * 10
                vel_r -= CHANGE_VALUE * 10
            elif vel_l == 0 and vel_r == 0 and key in ["left", "right"] and lastKey not in ["left", "right"]:
                if key == "right":
                    vel_l += CHANGE_VALUE * 5
                    vel_r -= CHANGE_VALUE * 5
                elif key == "left":
                    vel_l -= CHANGE_VALUE * 5
                    vel_r += CHANGE_VALUE * 5
            elif vel_l == vel_l and vel_r == vel_r:
                if vel_l > 0:
                    vel_l -= CHANGE_VALUE * 2
                elif vel_l < 0:
                    vel_l += CHANGE_VALUE * 2
                if vel_r > 0:
                    vel_r -= CHANGE_VALUE * 2
                elif vel_r < 0:
                    vel_r += CHANGE_VALUE * 2

            if vel_l > PWM_MAX or vel_l < PWM_MIN:
                vel_l = vel_l
            if vel_r > PWM_MAX or vel_r < PWM_MIN:
                vel_r = vel_r

            print(f"velocidade: left: {vel_l}  right: {vel_r}")
            setMotor(vel_l, vel_r)

            lastKey = key

        print(f"velocidade: left: {vel_l}  right: {vel_r}")
    print("Ending motor and closing")
    exit()

if __name__ == "__main__":
    controleStart()