from threading import Thread
import keyboard as kb
from controleMotor import setMotorLeft, setMotorRight, exit, setMotorMode 
import time

def controle():
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


controleMotorThread = Thread(target=controle)

controleMotorThread.start()