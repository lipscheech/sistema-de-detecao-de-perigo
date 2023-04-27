from threading import Thread
from controleMotor import controleStart 
import time

controleMotorThread = Thread(target=controleStart)

controleMotorThread.start()