import cv2
import numpy as np
import os
if os.name == 'nt': os.system('cls')
else : os.system("clear")

Img = cv2.imread("./Image_1.png")

hsvImg = cv2.cvtColor(Img, cv2.COLOR_BGR2HSV)

#マスク
lower_beige = np.array([10,50,50])      # 閾値の下限
upper_beige = np.array([30,255,255])    # 閾値の上限

mask_beige = cv2.inRange(hsvImg, lower_beige, upper_beige)
cv2.imshow("mask_beige",mask_beige)
cv2.waitKey(0)
cv2.imwrite('./Results/mask_beige.png', mask_beige)

print("END")