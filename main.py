from threading import Thread
import keyboard as kb
from controleMotor import controleStart 
import time

controleMotorThread = Thread(target=controleStart)

controleMotorThread.start()