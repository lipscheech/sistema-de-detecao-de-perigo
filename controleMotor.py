#!/usr/bin/env python
# coding: latin-1
# Autor:    Ingmar Stapel
# Datum:    20160731
# Version:    2.0
# Homepage:    http://custom-build-robots.com

from time import sleep
import RPi.GPIO as io
import numpy as np

io.setmode(io.BCM)

io.setwarnings(False)

L_L_EN = 18 # L_L_EN
L_R_EN = 17 # L_R_EN
io.setup(L_L_EN, io.OUT)
io.setup(L_R_EN, io.OUT)
io.output(L_L_EN, True)
io.output(L_R_EN, True)

R_L_EN = 6 # R_L_EN
R_R_EN = 12 # R_R_EN
io.setup(R_L_EN, io.OUT)
io.setup(R_R_EN, io.OUT)
io.output(R_L_EN, True)
io.output(R_R_EN, True)

L_L_PWM = 23 # leftmotorpwm_pin_l
L_R_PWM = 22 # leftmotorpwm_pin_r

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

def setMotorRight(power):
   int(power)
   if power < 0:
      # Rueckwaertsmodus fuer den rechten Motor
      #setMotorMode("rightmotor", "reverse")
      pwm = -int(PWM_MAX * power)
      if pwm > PWM_MAX:
         pwm = PWM_MAX
      rightmotorpwm_l.ChangeDutyCycle(pwm)
      rightmotorpwm_r.ChangeDutyCycle(0)
   elif power > 0:
      # Vorwaertsmodus fuer den rechten Motor
      #setMotorMode("rightmotor", "forward")
      pwm = int(PWM_MAX * power)
      if pwm > PWM_MAX:
         pwm = PWM_MAX
      rightmotorpwm_l.ChangeDutyCycle(0)
      rightmotorpwm_r.ChangeDutyCycle(pwm)
   else:
      # Stoppmodus fuer den rechten Motor
      rightmotorpwm_l.ChangeDutyCycle(0)
      rightmotorpwm_r.ChangeDutyCycle(0)
      
def setMotorLeft(power):
   int(power)
   if power < 0:
      # Rueckwaertsmodus fuer den linken Motor
      #setMotorMode("leftmotor", "reverse")
      pwm = -int(PWM_MAX * power)
      if pwm > PWM_MAX:
         pwm = PWM_MAX
      leftmotorpwm_l.ChangeDutyCycle(pwm)
      leftmotorpwm_r.ChangeDutyCycle(0)
   elif power > 0:
      # Vorwaertsmodus fuer den linken Motor
      #setMotorMode("leftmotor", "forward")
      pwm = int(PWM_MAX * power)
      if pwm > PWM_MAX:
         pwm = PWM_MAX
      leftmotorpwm_l.ChangeDutyCycle(0)
      leftmotorpwm_r.ChangeDutyCycle(pwm)
   else:
      # Stoppmodus fuer den linken Motor
      leftmotorpwm_l.ChangeDutyCycle(0)
      leftmotorpwm_r.ChangeDutyCycle(0)

def over(value, plus):
   value = value * 100 + plus
   if value > PWM_MAX:
       value = PWM_MAX
   elif value < -PWM_MAX:
       value = -PWM_MAX
   return np.round(value* .01, 2)

def exit():
    io.output(L_L_EN, False)
    io.output(L_R_EN, False)
    io.output(R_L_EN, False)
    io.output(R_R_EN, False)
    io.cleanup()

PWM_MAX = 80
PWM_MIN = 0
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
                vel_l = over(vel_l, -CHANGE_VALUE)
                vel_r = over(vel_r, CHANGE_VALUE)
            elif key == "down":
                vel_l = over(vel_l, CHANGE_VALUE)
                vel_r = over(vel_r, -CHANGE_VALUE)
            # elif key in ["left", "right"] and lastKey not in ["left", "right"]:
            #     if key == "right":
            #         vel_l += CHANGE_VALUE * 5
            #         vel_r -= CHANGE_VALUE * 5
            #     elif key == "left":
            #         vel_l -= CHANGE_VALUE * 5
            #         vel_r += CHANGE_VALUE * 5
            else:
                if vel_l > 0:
                    vel_l = over(vel_l, -CHANGE_VALUE)
                    vel_r = over(vel_r, -CHANGE_VALUE)
                elif vel_r < 0:
                    vel_l = over(vel_l, CHANGE_VALUE)
                    vel_r = over(vel_r, CHANGE_VALUE)

            print(f"velocidade: left: {vel_l}  right: {vel_r}")
            setMotorLeft(vel_l)
            setMotorRight(vel_r)

            lastKey = key

        print(f"velocidade: left: {vel_l}  right: {vel_r}")
    print("Ending motor and closing")
    exit()

if __name__ == "__main__":
    controleStart()