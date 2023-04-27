#!/usr/bin/env python
# coding: latin-1
# Autor:   Ingmar Stapel
# Datum:   20160731
# Version:   2.0
# Homepage:   http://custom-build-robots.com

# Dieses Programm wurde fuer die Ansteuerung der linken und rechten
# Motoren des Roboter-Autos entwickelt. Es geht dabei davon aus,
# dass eine L298N H-Bruecke als Motortreiber eingesetzt wird.

# Dieses Programm muss von einem uebergeordneten Programm aufgerufen
# werden, dass die Steuerung des Programmes L298NHBridge übernimmt.

# Es wird die Klasse RPi.GPIO importiert, die die Ansteuerung
# der GPIO Pins des Raspberry Pi ermoeglicht.
import RPi.GPIO as io
import keyboard as kb
import time
import numpy as np

io.setmode(io.BCM)

# Die Variable PWM_MAX gibt die maximale Drehgeschwindigkeit der
# Motoren als Prozentwert vor.
# Die Geschwindigkeit wird initial auf 70% der max Leistung der
# H-Bruecke gedrosselt um am Anfang mit der Steuerung des Roboter
# Autos besser zurecht zu kommen. Soll das Roboter-Auto schneller
# fahren kann hier der Wert von 70% auf maximal 100% gesetzt werden.

PWM_MAX = 100

# Mit dem folgenden Aufruf werden eventuelle Warnungen die die
# Klasse RPi.GPIO ausgibt deaktiviert.
io.setwarnings(False)

# Im folgenden Programmabschnitt wird die logische Verkabelung des
# Raspberry Pi im Programm abgebildet. Dazu werden den vom Motor
# Treiber bekannten Pins die GPIO Adressen zugewiesen.

# --- START KONFIGURATION GPIO Adressen ---

# Linker Motortreiber
L_L_EN = 22 # L_L_EN
L_R_EN = 23 # L_R_EN
L_L_PWM = 18 # leftmotorpwm_pin_l
L_R_PWM = 17 # leftmotorpwm_pin_r

# Rechter Motortreiber
R_L_EN = 13 # R_L_EN
R_R_EN = 19 # R_R_EN
R_L_PWM = 12 # rightmotorpwm_pin_l
R_R_PWM = 6 # rightmotorpwm_pin_r

io.setup(L_L_EN, io.OUT)
io.setup(L_R_EN, io.OUT)
io.output(L_L_EN, True)
io.output(L_R_EN, True)


io.setup(R_L_EN, io.OUT)
io.setup(R_R_EN, io.OUT)
io.output(R_L_EN, True)
io.output(R_R_EN, True)

io.setup(L_L_PWM, io.OUT)
io.setup(L_R_PWM, io.OUT)
leftmotorpwm_l = io.PWM(L_L_PWM,100)
leftmotorpwm_r = io.PWM(L_R_PWM,100)
leftmotorpwm_l.start(0)
leftmotorpwm_r.start(0)
leftmotorpwm_l.ChangeDutyCycle(0)
leftmotorpwm_r.ChangeDutyCycle(0)

io.setup(R_L_PWM, io.OUT)
io.setup(R_R_PWM, io.OUT)
rightmotorpwm_l = io.PWM(R_L_PWM,100)
rightmotorpwm_r = io.PWM(R_R_PWM,100)
rightmotorpwm_l.start(0)
rightmotorpwm_r.start(0)
rightmotorpwm_l.ChangeDutyCycle(0)
rightmotorpwm_r.ChangeDutyCycle(0)

# Die Funktion setMotorMode(motor, mode) legt die Drehrichtung der
# Motoren fest. Die Funktion verfügt über zwei Eingabevariablen.
# motor      -> diese Variable legt fest ob der linke oder rechte
#              Motor ausgewaehlt wird.
# mode      -> diese Variable legt fest welcher Modus gewaehlt ist
# Beispiel:
# setMotorMode(leftmotor, forward)   Der linke Motor ist gewaehlt
#                                   und dreht vorwaerts .
# setMotorMode(rightmotor, reverse)   Der rechte Motor ist ausgewaehlt
#                                   und dreht rueckwaerts.
# setMotorMode(rightmotor, stopp)   Der rechte Motor ist ausgewaehlt
#                                   der gestoppt wird.

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

# Die Funktion setMotorLeft(power) setzt die Geschwindigkeit der
# linken Motoren. Die Geschwindigkeit wird als Wert zwischen -1
# und 1 uebergeben. Bei einem negativen Wert sollen sich die Motoren
# rueckwaerts drehen ansonsten vorwaerts.
# Anschliessend werden aus den uebergebenen Werten die notwendigen
# %-Werte fuer das PWM Signal berechnet.

# Beispiel:
# Die Geschwindigkeit kann mit +1 (max) und -1 (min) gesetzt werden.
# Das Beispielt erklaert wie die Geschwindigkeit berechnet wird.
# SetMotorLeft(0)     -> der linke Motor dreht mit 0% ist gestoppt
# SetMotorLeft(0.75)  -> der linke Motor dreht mit 75% vorwaerts
# SetMotorLeft(-0.5)  -> der linke Motor dreht mit 50% rueckwaerts
# SetMotorLeft(1)     -> der linke Motor dreht mit 100% vorwaerts
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

# Die Funktion setMotorRight(power) setzt die Geschwindigkeit der
# rechten Motoren. Die Geschwindigkeit wird als Wert zwischen -1
# und 1 uebergeben. Bei einem negativen Wert sollen sich die Motoren
# rueckwaerts drehen ansonsten vorwaerts.
# Anschliessend werden aus den uebergebenen Werten die notwendigen
# %-Werte fuer das PWM Signal berechnet.

# Beispiel:
# Die Geschwindigkeit kann mit +1 (max) und -1 (min) gesetzt werden.
# Das Beispielt erklaert wie die Geschwindigkeit berechnet wird.
# setMotorRight(0)     -> der linke Motor dreht mit 0% ist gestoppt
# setMotorRight(0.75)  -> der linke Motor dreht mit 75% vorwaerts
# setMotorRight(-0.5)  -> der linke Motor dreht mit 50% rueckwaerts
# setMotorRight(1)     -> der linke Motor dreht mit 100% vorwaerts

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

# Die Funktion exit() setzt die Ausgaenge die den Motor Treiber
# steuern auf False. So befindet sich der Motor Treiber nach dem
# Aufruf derFunktion in einem gesicherten Zustand und die Motoren
# sind gestopped.
def exit():
   io.output(L_L_EN, False)
   io.output(L_R_EN, False)
   io.output(R_L_EN, False)
   io.output(R_R_EN, False)
   io.cleanup()

PWM_NOW = 25

def over(value, plus):
   value = value * 100 + plus
   if value > PWM_NOW:
       value = PWM_NOW
   elif value < -PWM_NOW:
       value = -PWM_NOW
   return np.round(value* .01, 2)

def controleStart():
      vel_l = 0
      vel_r = 0
      while True:
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

               setMotorLeft(.10)
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


# Ende des Programmes

if __name__ == "__main__":
    vel_l = 0
    vel_r = 0
    while True:
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

            setMotorLeft(.10)
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
