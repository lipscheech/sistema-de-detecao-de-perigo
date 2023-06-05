import matplotlib.pyplot as plt
from glob import glob
import cv2

imgs = sorted(glob("images/frame*"))
masks = sorted(glob("images/mask*"))

idx = 0
mask = cv2.imread(masks[idx])
img = cv2.imread(imgs[idx])

plt.imshow(img)

plt.imshow(mask)

plt.imshow(cv2.addWeighted(img, 0.75, mask, 0.25))

import numpy as np
np.unique(mask)

from generateAttentionArea import createAttetionArea
attetionArea = createAttetionArea((240, 320), top=150, bottom=230)[150:231, :]
plt.imshow(attetionArea)
cv2.imwrite("attentionArea.png", attetionArea)