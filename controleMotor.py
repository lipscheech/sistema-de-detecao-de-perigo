#!/usr/bin/env python
# coding: latin-1
# Autor:   Ingmar Stapel
# Datum:   20160731
# Version:   2.0
# Homepage:   http://custom-build-robots.com

import RPi.GPIO as io
import keyboard as kb
import time
import numpy as np

io.setmode(io.BCM)

PWM_MAX = 100

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
leftmotorpwm_l = io.PWM(L_L_PWM,100)
leftmotorpwm_r = io.PWM(L_R_PWM,100)
leftmotorpwm_l.start(0)
leftmotorpwm_r.start(0)
leftmotorpwm_l.ChangeDutyCycle(0)
leftmotorpwm_r.ChangeDutyCycle(0)

R_L_PWM = 13 # rightmotorpwm_pin_l
R_R_PWM = 19 # rightmotorpwm_pin_r

io.setup(R_L_PWM, io.OUT)
io.setup(R_R_PWM, io.OUT)
rightmotorpwm_l = io.PWM(R_L_PWM,100)
rightmotorpwm_r = io.PWM(R_R_PWM,100)
rightmotorpwm_l.start(0)
rightmotorpwm_r.start(0)
rightmotorpwm_l.ChangeDutyCycle(0)
rightmotorpwm_r.ChangeDutyCycle(0)

def setMotorMode(motor, mode):
   if motor == "leftmotor":
      if mode == "reverse":
         io.output(L_L_EN, True)
         io.output(L_R_EN, False)
      elif  mode == "forward":
         io.output(L_L_EN, False)
         io.output(L_R_EN, True)
      else:
         io.output(L_L_EN, False)
         io.output(L_R_EN, False)
   elif motor == "rightmotor":
      if mode == "reverse":
         io.output(R_L_EN, False)
         io.output(R_R_EN, True)
      elif  mode == "forward":
         io.output(R_L_EN, True)
         io.output(R_R_EN, False)
      else:
         io.output(R_L_EN, False)
         io.output(R_R_EN, False)
   else:
      io.output(L_L_EN, False)
      io.output(L_R_EN, False)
      io.output(R_L_EN, False)
      io.output(R_R_EN, False)

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

def exit():
   io.output(L_L_EN, False)
   io.output(L_R_EN, False)
   io.output(R_L_EN, False)
   io.output(R_R_EN, False)
   io.cleanup()

PWM_NOW = 50

def over(value, plus):
   value = value * 100 + plus
   if value > PWM_NOW:
       value = PWM_NOW
   elif value < -PWM_NOW:
       value = -PWM_NOW
   return np.round(value* .01, 2)

def controleStart(flag=None):
      vel_l = 0
      vel_r = 0
      while True:
         if flag.empty() or flag is None:
            #   input_ = input("set state:")
            if kb.is_pressed('space'):
                  setMotorLeft(0)
                  setMotorRight(0)
                  exit()
                  break
            elif kb.is_pressed('left'):
                  setMotorLeft(.05)
                  setMotorRight(.1)

            elif kb.is_pressed('up'):
                  vel_l = over(vel_l, 1)
                  vel_r = over(vel_r, 1)

                  setMotorLeft(vel_l)
                  setMotorRight(vel_r)
            
            elif kb.is_pressed('right'):

                  setMotorLeft(.1)
                  setMotorRight(.05)
            
            elif kb.is_pressed('down'):
                  vel_l = over(vel_l, -1)
                  vel_r = over(vel_r, -1)

                  setMotorLeft(vel_l)
                  setMotorRight(vel_r)
            else:
                  if vel_l > 0:
                     vel_l = over(vel_l, -1)
                     vel_r = over(vel_r, -1)
                  elif vel_r < 0:
                     vel_l = over(vel_l, 1)
                     vel_r = over(vel_r, 1)
                  setMotorLeft(vel_l)
                  setMotorRight(vel_r)
            print(vel_l, vel_r)
         time.sleep(.5)

if __name__ == "__main__":
   controleStart()