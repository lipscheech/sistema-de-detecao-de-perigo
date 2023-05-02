import cv2

cap = cv2.VideoCapture(0)

resolutions = {}

for width in range(0, 5000+1, 10):
    for height in range(0, 5000+1, 10):
        if 0 in [width, height]:
            continue
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        resolutions[str(width)+"x"+str(height)] = "OK"

print(resolutions)