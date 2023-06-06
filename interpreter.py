import cv2
from numpy import float32, uint8, expand_dims, argmax
from tensorflow.lite.python.interpreter import Interpreter
from generateAttentionArea import createAttetionArea
from time import time
import os
from datetime import datetime

# def postprocess(frame, mask, WIDTH, HEIGHT):
#     from PIL.Image import fromarray
#     from numpy import asarray, stack
#     from seaborn import color_palette

#     colorList = color_palette(None, 2)
#     colorListAux = []

#     for i in colorList:
#         colorListAux.append(int(i[0] * 255))
#         colorListAux.append(int(i[1] * 255))
#         colorListAux.append(int(i[2] * 255))
#     colorList = None

#     print(colorListAux)

#     mask = cv2.resize(mask, (WIDTH, HEIGHT), interpolation=cv2.INTER_NEAREST)
#     mask = stack([mask] * 3, axis=-1)
#     mask[mask == 1] = 255
#     mask = fromarray(mask, mode="P")
#     mask.putpalette(colorListAux)
#     mask = mask.convert("RGB")

#     return cv2.addWeighted(frame, .75, asarray(mask), .25, 0)

def run(PATH: str, FPS: int, imageSize: (int, int), THREAD: int, flag=None, quit=None):
    assert quit != None and flag != None
    #contSegmentation = 0
    print("Starting model load")
    interpreter = Interpreter(model_path=PATH, num_threads=THREAD)
    interpreter.allocate_tensors()
    print("Ending model load")
    #path = '/home/ubuntu/workspace/sistema-de-detecao-de-perigo/images'
    #arquivo = open("log.txt", "w")
    #dt = datetime.now()
    # arquivo.write("Iniciando o programa - "+str(dt.strftime('%c'))+"\n");

    flag.set()

    output_index = interpreter.get_output_details()[0]['index']
    input_index = interpreter.get_input_details()[0]['index']


    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, FPS)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, imageSize[1])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, imageSize[0])


    print(cap.get(cv2.CAP_PROP_FRAME_WIDTH),cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    attetionArea = createAttetionArea(imageSize, top=150, bottom=230)
    attentionPixels =  attetionArea.sum() * .8

    print("Starting model loop")
    while not quit.is_set():
        _, frame = cap.read()

        # PREPROCESS
        pre_frame = cv2.resize(frame, (imageSize[1], imageSize[0]), interpolation=cv2.INTER_AREA)
        pre_frame = cv2.cvtColor(pre_frame, cv2.COLOR_BGR2RGB).astype(float32)
        pre_frame = expand_dims(pre_frame, axis=0) / 127.5 - 1

        # INFERENCE
        interpreter.set_tensor(input_index, pre_frame)
        frame_time = time()
        interpreter.invoke() 
        fps = 1 / (time() - frame_time)
        mask = interpreter.get_tensor(output_index)[0].astype(uint8)
        # mask = argmax(mask, axis=-1)
        
        # cv2.imwrite(os.path.join(path, "frame"+str(contSegmentation)+".png"), frame)
        # cv2.imwrite(os.path.join(path,"mask"+str(contSegmentation)+".png"), mask)
        mask = (mask * attetionArea).sum()

        # POSTPROCESS
        if mask <= attentionPixels:
            if ~flag.is_set():
                print("setting block")
                flag.set()
        elif flag.is_set():
            print("setting free")
            flag.clear()


        print(f"fps:{fps} blocked: {flag.is_set()}" )

        #contSegmentation += 1
        # arquivo.write("FPS: "+str(fps)+"\n");

    #dt = datetime.now()
    # arquivo.write("Finalizando o programa - "+str(dt.strftime('%c'))+"\n")
    #arquivo.close()
    print("Ending model loop")
    cap.release()
    cv2.destroyAllWindows()

# if __name__ == '__main__':
#     from argparse import ArgumentParser

#     parser = ArgumentParser()
#     parser.add_argument(
#         "--path", default="model.tflite", help="path to model")
#     parser.add_argument('--camera_width', type=int, default=320,
#                         help='USB Camera resolution (width). (Default=640)')
#     parser.add_argument('--camera_height', type=int, default=240,
#                         help='USB Camera resolution (height). (Default=360)')
#     parser.add_argument('--cam_fps', type=int, default=30,
#                         help='FPS (Default=15)')
#     parser.add_argument("--thread", type=int, default=4,
#                         help="Number of Threads")
#     args = parser.parse_args()

#     run(PATH=args.path, FPS=args.cam_fps, WIDTH=args.camera_width, HEIGHT=args.camera_height, THREAD=args.thread)