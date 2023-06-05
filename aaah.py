import cv2
from numpy import float32, uint8, expand_dims
from tensorflow.lite.python.interpreter import Interpreter

def run(PATH: str, img, normalize=1, offset=0):
    interpreter = Interpreter(model_path=PATH, num_threads=4)
    interpreter.allocate_tensors()

    output_index = interpreter.get_output_details()[0]['index']
    input_index = interpreter.get_input_details()[0]['index']

    pre_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(float32)
    pre_frame = expand_dims(pre_frame, axis=0) / normalize - offset

    # INFERENCE
    interpreter.set_tensor(input_index, pre_frame)
    interpreter.invoke()
    return interpreter.get_tensor(output_index)[0].astype(uint8)