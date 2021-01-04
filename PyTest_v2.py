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
originalImg = cv2.imread("./Input_IMG/DSC_0041.jpg")
# 座標指定：[左上],[右上],[右下],[左下]
ptlist = [1125,249],[2734,105],[2744,1822],[1101,1717]
cv2.namedWindow("originalImg", cv2.WINDOW_NORMAL)   # 画像がデカすぎるので縮小表示用
cv2.imshow("originalImg",originalImg)
cv2.waitKey(0)

pts = np.array(ptlist, np.int32)
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

# BGR→GRAY変換
GRAYImg = cv2.cvtColor(boardImg, cv2.COLOR_BGR2GRAY)
cv2.imshow("GRAYImg",GRAYImg)
cv2.waitKey(0)
cv2.imwrite('./Results/GRAYImg.png', GRAYImg)

# ノイズ処理
kernelSize = 25
noiseReducedImg = cv2.medianBlur(GRAYImg,kernelSize)
cv2.imshow("noiseReducedImg",noiseReducedImg)
cv2.waitKey(0)
cv2.imwrite('./Results/noiseReducedImg.png', noiseReducedImg)

# 結果に重ねる用の，カラー画像に変換したnoiseReducedImg(GRAY)
GRAY_to_COLOR = cv2.cvtColor(noiseReducedImg, cv2.COLOR_GRAY2BGR)

# 交点付与（これ自体はなくてもいいが，取得領域の確認用）
boardWithPointsImg = MOD.drawXP_Rect(GRAY_to_COLOR)
cv2.imshow("boardWithPointsImg",boardWithPointsImg)
cv2.waitKey(0)
cv2.imwrite('./Results/boardWithPointsImg.png', boardWithPointsImg)


# ――マスク処理編――
'''
mask_BLACK = cv2.inRange(GRAYImg, 0, 50)    # 黒石抽出 0～50
cv2.imshow("mask_BLACK",mask_BLACK)
cv2.waitKey(0)
cv2.imwrite('./Results/mask_BLACK.png', mask_BLACK)

mask_WHITE = cv2.inRange(GRAYImg, 160, 255)    # 白石抽出 160～255
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


stonePosition = MOD.checkStonePosition(res) # resはマスク付き, noiseReducedImgと比較しろ
# print(re.sub("[|[[|]|]|],", "", str(stonePosition).replace("], [","], \n[")))
# stonePosition の情報を.csvに保存
with open('./Results/stonePosition.csv', 'w', newline="") as f:
    writer = csv.writer(f)
    writer.writerows(stonePosition)

# 結果
resultWithNoiseReducedImg = MOD.drawTerritoryColor(res,stonePosition)
cv2.imshow("resultWithNoiseReducedImg",resultWithNoiseReducedImg)
cv2.waitKey(0)
cv2.imwrite('./Results/resultWithNoiseReducedIMG.png', resultWithNoiseReducedImg)
'''
stonePosition_NoMask = MOD.checkStonePosition(noiseReducedImg) 
result_noiseReduced = MOD.drawTerritoryColor(GRAY_to_COLOR,stonePosition_NoMask)
cv2.imshow("result_noiseReduced",result_noiseReduced)
cv2.waitKey(0)
cv2.imwrite('./Results/result_noiseReduced.png', result_noiseReduced)

result = MOD.drawTerritoryColor(boardImg,stonePosition_NoMask)
cv2.imshow("result",result)
cv2.waitKey(0)
cv2.imwrite('./Results/result.png', result)

# 結果
# resultImg = MOD.drawTerritoryColor(boardImg,stonePosition)
# cv2.imshow("resultImg",resultImg)
# cv2.waitKey(0)
# cv2.imwrite('./Results/resultIMG.png', resultImg)

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