from threading import Thread, Event
from controleMotor import controleStart
from interpreter import run
from queue import Queue
from keyboard import is_pressed

flag = Event()
quit = Event()
key = Queue(1)

print("Creating Model Thread")

startInterpreterThread = Thread(
    target=run,
    args=([
    "fold_0_alpha_0.5_lr_1e-04_regularizer_l1_1e-04_l2_1e-05.tflite",
    30, 320, 240, 4, flag, quit])
    )

print("Creating Motor Thread")

controleMotorThread = Thread(
    target=controleStart,
    args=([key, flag, quit])
    )



print("Starting Model Thread")
startInterpreterThread.start()

flag.wait()

print("Starting Motor Thread")

controleMotorThread.start()

flag.wait()

print("Starting main loop")
while True:
    try:
        if is_pressed('left'):
            key.put('left')
        elif is_pressed('up'):
            key.put('up')
        elif is_pressed('right'):
            key.put('right')
        elif is_pressed('down'):
            key.put('down')
        else:
            key.put('none')
    except:
        pass

    if is_pressed("space"):
        break

print("Ending main loop")

quit.set()