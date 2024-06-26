# -*- coding: utf-8 -*-


import cv2
import numpy as np
import matplotlib.pyplot as plt
import torch

# Load images
image1 = cv2.imread('/content/000000.png', cv2.IMREAD_GRAYSCALE)
image2 = cv2.imread('/content/000023.png', cv2.IMREAD_GRAYSCALE)

# Load the Fundamental matrix F
F=np.array([[3.34638533e-07,7.58547151e-06,-2.04147752e-03],[-5.83765868e-06,1.36498636e-06,2.67566877e-04],[1.45892349e-03,4.37648316e-03,1.00000000e+00]])
#F=torch.from_numpy(F).float()

# Find epipolar lines
lines1 = cv2.computeCorrespondEpilines(np.array([[10, 10]], dtype=np.float32), 1, F)
lines1 = lines1.reshape(-1, 3)

lines2 = cv2.computeCorrespondEpilines(np.array([[10, 10]], dtype=np.float32), 2, F)
lines2 = lines2.reshape(-1, 3)

# Extract epipolar lines
def extract_epipolar_line(img, line):
    _, w = img.shape
    a, b, c = line
    x0, y0 = map(int, [0, -c/b])
    x1, y1 = map(int, [w, -(a*w+c)/b])
    return (x0, y0), (x1, y1)

epiline1 = extract_epipolar_line(image1, lines1[0])
epiline2 = extract_epipolar_line(image2, lines2[0])

# Visualize epipolar lines
plt.figure(figsize=(16, 7))

plt.subplot(1, 2, 1)
plt.imshow(image1, cmap='gray')
plt.plot([epiline1[0][0], epiline1[1][0]], [epiline1[0][1], epiline1[1][1]], color='red')
plt.title('Epipolar Line in Image 1')

plt.subplot(1, 2, 2)
plt.imshow(image2, cmap='hot')
plt.plot([epiline2[0][0], epiline2[1][0]], [epiline2[0][1], epiline2[1][1]], color='g')
plt.title('Epipolar Line in Image 2')

plt.tight_layout()
plt.show()
