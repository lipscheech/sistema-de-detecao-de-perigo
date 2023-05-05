from threading import Thread, Event
from controleMotor import controleStart
from keyboard import is_pressed
from interpreter import run
from queue import Queue
from time import sleep

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
flag.clear()

print("Starting Motor Thread")

controleMotorThread.start()

print("Starting main loop")
while not is_pressed("space"):
    try:
        if is_pressed('left'):
            key.put_nowait('left')
            print("left")
        elif is_pressed('up'):
            key.put_nowait('up')
            print("up")
        elif is_pressed('right'):
            key.put_nowait('right')
            print("right")
        elif is_pressed('down'):
            key.put_nowait('down')
            print("down")
        else:
            key.put_nowait('none')
    except:
        pass

    sleep(.25)

print("Ending main loop")

quit.set()