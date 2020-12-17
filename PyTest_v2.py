# 本当にこんなにインポートする必要があるのかは分からない．減らせるかもしれない．
import cv2
import numpy as np
import matplotlib.pyplot as plt
import re
import csv
import Module as MOD    # 関数部分を1つのファイルに分けた．使い回せるように．
import os   # OSに限らず，この下の3行で実行時にコンソール内容を消去する．
if os.name == 'nt': os.system('cls')
else : os.system("clear")

#           --- 処理開始 ---

# ファイル指定と、指定ファイルの表示
# originalImg = cv2.imread("./Input_IMG/DSC_0041.jpg")
originalImg = cv2.imread("./Input_IMG/DSC_0170.jpg")
cv2.namedWindow("originalImg", cv2.WINDOW_NORMAL)   # 画像がデカすぎるので縮小表示用
cv2.imshow("originalImg",originalImg)
cv2.waitKey(0)

# 座標指定：[左上],[右上],[右下],[左下]
pts = np.array([[]], np.int32)
# pts = np.array([[1126,250],[2735,105],[2745,1818],[1103,1711]], np.int32)
cornerOfGoBoard = np.float32(pts) # float32に型変換。透視変換行列の計算で必要になる。
cornerOfImage = np.float32([[0,0], [800,0], [800,800], [0, 800]])

# 切り抜き領域可視化
cornerImg = MOD.drawCorner(originalImg,pts)
for p in pts:
    cv2.drawMarker(cornerImg, (p[0],p[1]), (0, 255, 0), cv2.MARKER_TILTED_CROSS, 50, 10)
cv2.namedWindow("cornerImg", cv2.WINDOW_NORMAL)
cv2.imshow("cornerImg",cornerImg)
cv2.waitKey(0)
cv2.imwrite('./Results/cornerImg.png', cornerImg)

# 透視変換(Perspective Transform)
boardImg = MOD.perspectiveTransform(originalImg, cornerOfGoBoard, cornerOfImage)
cv2.imshow("Results/boardImg",boardImg)
cv2.waitKey(0)
cv2.imwrite('./Results/boardImg.png', boardImg)

# 交点付与
boardWithPointsImg = MOD.drawCrossPoints(boardImg)
cv2.imshow("boardWithPointsImg",boardWithPointsImg)
cv2.waitKey(0)
cv2.imwrite('./Results/boardWithPointsImg.png', boardWithPointsImg)

# ノイズ処理
# noiseReducedImg = MOD.reduceNoise(boardImg, 37, 0)
noiseReducedImg = cv2.GaussianBlur(boardImg,(11,11),0)
cv2.imshow("noiseReducedImg",noiseReducedImg)
cv2.waitKey(0)
cv2.imwrite('./Results/noiseReducedImg.png', noiseReducedImg)

# # 確認用の表示(BGR→HSV変換)
# hsvImg = cv2.cvtColor(noiseReducedImg, cv2.COLOR_BGR2HSV)
# cv2.imshow("hsvImg",hsvImg)
# cv2.waitKey(0)
# cv2.imwrite('./Results/hsvImg.png', hsvImg)

# 確認用の表示(BGR→HSV変換)
GRAYImg = cv2.cvtColor(noiseReducedImg, cv2.COLOR_BGR2GRAY)
cv2.imshow("GRAYImg",GRAYImg)
cv2.waitKey(0)
cv2.imwrite('./Results/GRAYImg.png', GRAYImg)

#マスク
# beige = np.uint8([[[61,91,146]]])                   # これ使われてない
# hsv_beige = cv2.cvtColor(beige,cv2.COLOR_BGR2HSV)   # これ使われてない……
lower_BLACK = np.array([0,0,0])      # 閾値の下限
upper_BLACK = np.array([360,100,100])    # 閾値の上限

mask_BLACK = cv2.inRange(GRAYImg, 0, 50)    # 黒石抽出
cv2.imshow("mask_BLACK",mask_BLACK)
cv2.waitKey(0)
cv2.imwrite('./Results/mask_BLACK.png', mask_BLACK)

mask_WHITE = cv2.inRange(GRAYImg, 160, 255)    # 黒石抽出
cv2.imshow("mask_WHITE",mask_WHITE)
cv2.waitKey(0)
cv2.imwrite('./Results/mask_WHITE.png', mask_WHITE)

mask = cv2.bitwise_or(mask_BLACK,mask_WHITE)
cv2.imshow("mask",mask)
cv2.waitKey(0)
cv2.imwrite('./Results/mask.png', mask)

# # ネガポジ
# mask_negaposi = cv2.bitwise_not(mask)
# cv2.imshow("mask_negaposi",mask_negaposi)
# cv2.waitKey(0)
# cv2.imwrite('./Results/mask_negaposi.png', mask_negaposi)

# 結果
res = cv2.bitwise_and(boardImg,boardImg, mask= mask)
cv2.imshow("res",res)
cv2.waitKey(0)
cv2.imwrite('./Results/res.png', res)


# resに点を付与
resWithPointsImg = MOD.drawXP_Rect(res)
cv2.imshow("resWithPointsImg",resWithPointsImg)
cv2.waitKey(0)
cv2.imwrite('./Results/resWithPointsImg.png', resWithPointsImg)

stonePosition = MOD.checkStonePosition(res)
# print(re.sub("[|[[|]|]|],", "", str(stonePosition).replace("], [","], \n[")))
# stonePosition の情報を.csvに保存
with open('./Results/stonePosition.csv', 'w', newline="") as f:
    writer = csv.writer(f)
    writer.writerows(stonePosition)

# 結果
resultWithNoiceReducedImg = MOD.drawTerritoryColor(noiseReducedImg,stonePosition)
cv2.imshow("resultWithNoiceReducedImg",resultWithNoiceReducedImg)
cv2.waitKey(0)
cv2.imwrite('./Results/resultWithNoiceReducedIMG.png', resultWithNoiceReducedImg)

# 結果
resultImg = MOD.drawTerritoryColor(boardImg,stonePosition)
cv2.imshow("resultImg",resultImg)
cv2.waitKey(0)
cv2.imwrite('./Results/resultIMG.png', resultImg)

print("END")

'''
with open('./Results/dummyPosition.csv', 'r', newline="") as f: # 偽の碁盤情報をdummyPosition.csvから取得，比較を行う
    reader = csv.reader(f)
    l = [row for row in reader]
    # ndarrayを比較演算子で比較すると，各要素に対して一致してるかどうかの真理値を返す．
    compare = np.array(stonePosition) == np.array(l)    
    # 比較結果を画像に重ねる．
    resultDummyCompare = MOD.drawCompareStone(boardImg, compare)
    cv2.imshow("compare", resultDummyCompare)
    cv2.waitKey(0)
'''