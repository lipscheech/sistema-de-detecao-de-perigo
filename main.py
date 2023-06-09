from threading import Thread, Event
from controleMotor import controleStart
from keyboard import is_pressed
from interpreter import run
from queue import Queue
from time import sleep

flag = Event()
quit = Event()
key = Queue(100)

print("Creating Model Thread")

startInterpreterThread = Thread(
    target=run,
    args=([
    "model_5_vFlip_False.tflite",
    30, (240, 320), 4, flag, quit])
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

    sleep(.5)

print("Ending main loop")

quit.set()