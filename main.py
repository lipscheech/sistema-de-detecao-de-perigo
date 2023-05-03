from threading import Thread
from controleMotor import controleStart
from interpreter import startInterpreter 

controleMotorThread = Thread(target=controleStart)
startInterpreterThread = Thread(target=startInterpreter)

controleMotorThread.start()