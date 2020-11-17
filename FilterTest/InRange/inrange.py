import cv2
import numpy as np
import os
if os.name == 'nt': os.system('cls')
else : os.system("clear")

Img = cv2.imread("./Image_1.png")

hsvImg = cv2.cvtColor(Img, cv2.COLOR_BGR2HSV)

#マスク
upper= np.array([360,100,100])    # 閾値の上限
lower= np.array([0,0,0])      # 閾値の下限

mask= cv2.inRange(hsvImg, lower, upper)
cv2.imshow("mask",mask)
cv2.waitKey(0)
cv2.imwrite('./Res_mask.png', mask)

print("END")