from threading import Thread, Event
from controleMotor import controleStart
from interpreter import run
from queue import Queue
import keyboard as kb

flag = Event()
quit = Event()
key = Queue(1)

controleMotorThread = Thread(
    target=controleStart,
    args=([key, flag, quit])
    )

startInterpreterThread = Thread(
    target=run,
    args=([
    "fold_0_alpha_0.5_lr_1e-04_regularizer_l1_1e-04_l2_1e-05.tflite",
    30, 320, 240, 4, flag, quit])
    )

controleMotorThread.start()
startInterpreterThread.start()

while True:
    try:
        if kb.is_pressed('left'):
            key.put('left')
        elif kb.is_pressed('up'):
            key.put('up')
        elif kb.is_pressed('right'):
            key.put('right')
        elif kb.is_pressed('down'):
            key.put('down')
        else:
            key.put('none')
    except:
        pass

    if kb.is_pressed("space"):
        break

quit.set()