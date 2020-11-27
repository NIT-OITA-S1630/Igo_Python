import cv2
import numpy as np
import matplotlib.pyplot as plt
import re
import csv
import sys
import os
if os.name == 'nt': os.system('cls')
else : os.system("clear")

args = sys.argv

#           --- 処理開始 ---

# ファイル指定と、指定ファイルの表示
filename_1 = "./Data/Fig1.jpg"
InputImg_1 = cv2.imread(filename_1)

filename_2 = "./Data/Fig2.jpg"
InputImg_2 = cv2.imread(filename_2)

# BGR→HSV変換
HSV_Img_1 = cv2.cvtColor(InputImg_1, cv2.COLOR_BGR2HSV)
cv2.namedWindow("HSV_Img_1", cv2.WINDOW_NORMAL)   # 画像がデカすぎるので縮小表示用
cv2.imwrite('./HSV/Img_1.png', HSV_Img_1)

# BGR→HLS変換
HLS_Img_1 = cv2.cvtColor(InputImg_1, cv2.COLOR_BGR2HLS)
cv2.namedWindow("HLS_Img_1", cv2.WINDOW_NORMAL)   # 画像がデカすぎるので縮小表示用
cv2.imwrite('./HLS/Img_1.png', HLS_Img_1)


# BGR→XYZ変換
XYZ_Img_1 = cv2.cvtColor(InputImg_1, cv2.COLOR_BGR2XYZ)
cv2.namedWindow("XYZ_Img_1", cv2.WINDOW_NORMAL)   # 画像がデカすぎるので縮小表示用
cv2.imwrite('./XYZ/Img_1.png', XYZ_Img_1)

HSV_Img_2 = cv2.cvtColor(InputImg_2, cv2.COLOR_BGR2HSV)
cv2.namedWindow("HSV_Img_2", cv2.WINDOW_NORMAL)   # 画像がデカすぎるので縮小表示用
cv2.imwrite('./HSV/Img_2.png', HSV_Img_2)

HLS_Img_2 = cv2.cvtColor(InputImg_2, cv2.COLOR_BGR2HLS)
cv2.namedWindow("HLS_Img_2", cv2.WINDOW_NORMAL)   # 画像がデカすぎるので縮小表示用
cv2.imwrite('./HLS/Img_2.png', HLS_Img_2)

XYZ_Img_2 = cv2.cvtColor(InputImg_2, cv2.COLOR_BGR2XYZ)
cv2.namedWindow("XYZ_Img_2", cv2.WINDOW_NORMAL)   # 画像がデカすぎるので縮小表示用
cv2.imwrite('./XYZ/Img_2.png', XYZ_Img_2)

print("END")
'''
#マスク
beige = np.uint8([[[61,91,146]]])       # BGRでマスク色を指定
hsv_beige = cv2.cvtColor(beige,cv2.COLOR_BGR2HSV)
lower_beige = np.array([10,50,50])      # 閾値の下限
upper_beige = np.array([30,255,255])    # 閾値の上限

mask_beige = cv2.inRange(hsvImg, lower_beige, upper_beige)
cv2.imshow("mask_beige",mask_beige)
cv2.waitKey(0)

# ネガポジ
mask_negaposi = cv2.bitwise_not(mask_beige)
cv2.imshow("mask_negaposi",mask_negaposi)
cv2.waitKey(0)
cv2.imwrite('./Results/mask_negaposi.png', mask_negaposi)

# 結果
res = cv2.bitwise_and(boardImg,boardImg, mask= mask_negaposi)
cv2.imshow("res",res)
cv2.waitKey(0)
cv2.imwrite('./Results/res.png', res)


# resに点を付与
resWithPointsImg = drawXP_Rect(res)
cv2.imshow("resWithPointsImg",resWithPointsImg)
cv2.waitKey(0)
cv2.imwrite('./Results/resWithPointsImg.png', resWithPointsImg)

stonePosition = checkStonePosition(res)
# print(re.sub("[|[[|]|]|],", "", str(stonePosition).replace("], [","], \n[")))
# stonePosition の情報を.csvに保存
with open('./Results/stonePosition.csv', 'w', newline="") as f:
    writer = csv.writer(f)
    writer.writerows(stonePosition)

# print("stonePosition: \n" + str(stonePosition).replace("], [","], \n[") + "\n")

# 結果
resultImg = drawTerritoryColor(boardImg,stonePosition)
cv2.imshow("resultImg",resultImg)
cv2.waitKey(0)
cv2.imwrite('./Results/resultIMG.png', resultImg)

'''

'''
# 偽の碁盤情報を用意、stonePositionと比較
dummy = [[1, 0, 0, 255, 255, -1, -1, -1, -1, -1, -1, -1, -1, -1, 255, 255, 255, 255, 0], 
[-1, 0, 255, 255, -1, 255, -1, -1, -1, -1, -1, 255, 255, -1, 255, 0, 255, 0, 0], 
[-1, 0, 255, 0, 255, 255, -1, -1, -1, 255, 255, 0, 255, 255, 0, 0, 0, 0, -1], 
[-1, -1, 0, 0, 0, 255, 255, 255, 255, 0, 0, 0, 255, 0, 0, 0, 0, -1, -1], 
[-1, -1, 0, 255, 255, 0, 0, 0, 0, 0, -1, 0, 255, 0, 255, 255, 0, -1, -1], 
[-1, -1, 0, 255, 255, 255, 0, 255, 0, 255, 0, -1, 0, 0, 255, 255, 0, -1, -1], 
[-1, -1, -1, 0, 0, 255, 255, 255, 255, 255, 0, 0, 255, 255, 255, 0, -1, -1, -1], 
[-1, -1, 0, 0, 255, -1, 255, 0, 0, 0, 0, 0, 255, 0, 255, 0, 0, 0, 0], 
[-1, -1, 0, 255, 255, -1, 255, 0, 0, 255, 255, 0, 255, 0, 255, 255, 0, 255, 0], 
[-1, 0, 255, -1, -1, -1, 255, 255, 0, 0, 255, 0, 0, 0, 0, 255, 0, 255, 255], 
[-1, 0, 255, -1, -1, -1, 255, 0, 0, 0, 255, 255, 255, 255, 255, 0, -1, 255, -1], 
[0, 0, 255, -1, -1, 255, 0, 0, 255, 255, -1, -1, -1, -1, -1, -1, 255, -1, -1], 
[255, 0, 255, 255, 255, 255, 255, 255, 255, 0, -1, -1, -1, -1, -1, 255, 0, 255, 255], 
[255, 255, 255, 0, 0, 0, 255, 0, 0, 255, 255, -1, -1, -1, -1, 255, 0, 255, 255], 
[-1, 255, 0, 0, 0, 0, 0, -1, 0, 255, 255, -1, -1, -1, 255, 0, 0, 0, 255], 
[255, 255, 255, 255, 255, 0, -1, 0, -1, 0, 0, 255, 255, 255, 255, 255, 0, 0, 255], 
[0, 255, 0, 255, 255, 0, -1, 255, 0, 0, 0, 255, 0, 0, 255, 255, 255, 0, 0], 
[0, 0, 0, 0, 0, -1, -1, -1, -1, -1, 0, 0, -1, 0, 0, 255, 0, 0, -1], 
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1]]

compare = np.array(stonePosition) == np.array(dummy)
resultDummyCompare = drawCompareStone(boardImg, compare)
cv2.imshow("compare", resultDummyCompare)
cv2.waitKey(0)
'''