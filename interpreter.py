import cv2
from numpy import float32, uint8, expand_dims
from tensorflow.lite.python.interpreter import Interpreter
from PIL.Image import fromarray
from time import time
import keyboard as kb

def postprocess(frame, mask, WIDTH, HEIGHT):
    from numpy import asarray, stack
    from seaborn import color_palette

    colorList = color_palette(None, 2)
    colorListAux = []

    for i in colorList:
        colorListAux.append(int(i[0] * 255))
        colorListAux.append(int(i[1] * 255))
        colorListAux.append(int(i[2] * 255))
    colorList = None

    print(colorListAux)

    mask = cv2.resize(mask, (WIDTH, HEIGHT), interpolation=cv2.INTER_NEAREST)
    mask = stack([mask] * 3, axis=-1)
    mask[mask == 1] = 255
    mask = fromarray(mask, mode="P")
    mask.putpalette(colorListAux)
    mask = mask.convert("RGB")

    return cv2.addWeighted(frame, .75, asarray(mask), .25, 0)

def run(PATH: str, FPS: int, WIDTH: int, HEIGHT: int, THREAD: int, flag=None):
    interpreter = Interpreter(model_path=PATH, num_threads=THREAD)
    interpreter.allocate_tensors()

    output_index = interpreter.get_output_details()[0]['index']
    input_index = interpreter.get_input_details()[0]['index']
    input_w, input_h = interpreter.get_input_details()[0]["shape"][1:3]

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, FPS)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

    while cap.isOpened():
        frame_time = time()

        _, frame = cap.read()

        # PREPROCESS
        pre_frame = cv2.resize(frame, (input_w, input_h), interpolation=cv2.INTER_AREA).astype(float32)
        pre_frame = cv2.cvtColor(pre_frame, cv2.COLOR_BGR2RGB)
        pre_frame = expand_dims(pre_frame, axis=0) / 127.5 - 1

        # INFERENCE
        interpreter.set_tensor(input_index, pre_frame)
        interpreter.invoke()
        mask = interpreter.get_tensor(output_index)[0].astype(uint8)

        # POSTPROCESS
        # image = postprocess(frame, mask, WIDTH, HEIGHT)
        
        condition = True
        if flag is not None:
            if kb.is_pressed('space') and flag.empty():
                print("Escrevendo na fila")
                flag.put(1)
            elif ~flag.empty():
                print("Limpando fila")
                flag.get()

        fps = 1 / (time() - frame_time)

        print(fps)
        # cv2.putText(image, str(fps), (5, 16),
        #             cv2.FONT_HERSHEY_SIMPLEX, .75, (255, 255), 3, cv2.LINE_AA)

        # cv2.imshow("segmentation", image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument(
        "--path", default="model.tflite", help="path to model")
    parser.add_argument('--camera_width', type=int, default=320,
                        help='USB Camera resolution (width). (Default=640)')
    parser.add_argument('--camera_height', type=int, default=240,
                        help='USB Camera resolution (height). (Default=360)')
    parser.add_argument('--cam_fps', type=int, default=30,
                        help='FPS (Default=15)')
    parser.add_argument("--thread", type=int, default=4,
                        help="Number of Threads")
    args = parser.parse_args()

    run(PATH=args.path, FPS=args.cam_fps, WIDTH=args.camera_width, HEIGHT=args.camera_height, THREAD=args.thread)