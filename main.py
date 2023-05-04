from threading import Thread, RLock
from controleMotor import controleStart
from interpreter import run
from queue import Queue

lockControl = RLock()
flag = Queue(1)

controleMotorThread = Thread(
    target=controleStart,
    args=([flag])
    )

startInterpreterThread = Thread(
    target=run,
    args=([
    "fold_0_alpha_0.5_lr_1e-04_regularizer_l1_1e-04_l2_1e-05.tflite",
    30, 320, 240, 4, flag])
    )

controleMotorThread.start()
startInterpreterThread.start()