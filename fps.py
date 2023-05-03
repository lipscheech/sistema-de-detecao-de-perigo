import cv2

cap = cv2.VideoCapture(0)

fps_dict = {}

for i in range(1, 81):
    cap.set(cv2.CAP_PROP_FPS, i)
    fps = cap.get(cv2.CAP_PROP_FPS)
    fps_dict[fps] = "OK"

print(fps_dict)
cap.release()