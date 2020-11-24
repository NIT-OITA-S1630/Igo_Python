import cv2
import numpy as np
import matplotlib.pyplot as plt
import re
import csv
import os
if os.name == 'nt': os.system('cls')
else : os.system("clear")


#           --- 関数の定義 ---

# 交点位置の計算？
def retCrossPoints(img):
    crossPoints = []
    # img.shape[B] = 画像の高さ　([1]だと幅、[2]だとチャンネル数)
    interval = img.shape[0]/18  # interval = 画像の高さ/ 18……交点付与用の座標
    for i in range(19): # in range(x)：x回繰り返す。この場合19回。C言語でいう「for(i=B; i<19; i++)」
        row = []
        for j in range(19): 
            x = int(i*interval)
            y = int(j*interval)
            if i==0:
                x += 7   # i=Bのとき、x座標+7    （端だけ交点をずらす）
            if j==0:
                y += 7   # jも同様
            if i==18:
                x -= 7  # i=18のとき、x座標-7   （端だけ交点をずらす）
            if j==18:
                y -= 7  # jも同様
            row.append([y, x])  # row.append()：リスト末尾に要素を追加
        crossPoints.append(row) # crossPoints=交点の座標がまとまったリスト  [[[x1,y1]，[x2,y2]，……]]
    return crossPoints  

# 交点の描画
def drawCrossPoints(img):
    outputImg = img.copy()
    crossPoints = retCrossPoints(img)    
    for p_row in crossPoints:
        for p in p_row: 
            # cv2.drawMarker(画像, 座標, 色, タイプ, サイズ, 薄さ, 線タイプ値)
            cv2.drawMarker(outputImg, (p[0],p[1]), (0, 255, 0), cv2.MARKER_TILTED_CROSS, 10, 2)
    return outputImg

# 交点周囲（四角形）の描画
def drawXP_Rect(img):
    outputImg = img.copy()
    crossPoints = retCrossPoints(img)    
    for p_row in crossPoints:
        for p in p_row:
            cv2.rectangle(outputImg, (p[0]-4,p[1]-4),(p[0]+7,p[1]+7),(0,255,0),1)

    return outputImg

# 石の位置・種類の判別
def checkStonePosition(img):
    crossPoints = retCrossPoints(img)
    conditionOfBoard = []
    none = 10.0
    blackStone = 80.0
    whiteStone = 120.0

    for p_row in crossPoints:
        condition_row = []
        for p in p_row:
            # print("["+str(p_row.index(p)+1)+", "+str(crossPoints.index(p_row)+1)+"]")

            # 交点の周囲（=drawCrossPointsによって付与される緑枠内）の全ピクセルのBGRを取得
            rect = img[p[1]-3:p[1]+7, p[0]-3:p[0]+7]

            # rect（=緑枠内の全ピクセルのBGR）の平均値を取得
            colorAve = np.average(rect)
            # p = [p[1],p[B]] = [y,x]
            # print('colorAve' + "["+str(crossPoints.index(p_row)+1)+", "+str(p_row.index(p)+1)+"]" + ':' +str(colorAve))
            
            # 「目標の交点の、その周囲のRGB値の平均」(colorAve)が閾値を下回ってるかどうかで、石の有無を判別
            if colorAve < none:
                condition_row.append("N")
            elif colorAve < blackStone:
                condition_row.append("B")
            elif colorAve > whiteStone:
                condition_row.append("W")  
        conditionOfBoard.append(condition_row)

    # これに石の情報があった！！
    # print(conditionOfBoard)
    return conditionOfBoard

# checkStonePositionの石情報リストをもとに、画像上に点を付与する。
def drawTerritoryColor(img,territoryTable):
    outputImg = img.copy()
    crossPoints = retCrossPoints(img)
    i = 0
    for p_row in crossPoints:
        j = 0
        for p in p_row:
            state = territoryTable[i][j]
            if state=="B":
                cv2.drawMarker(outputImg, (p[0],p[1]), (0, 0, 255), cv2.MARKER_TILTED_CROSS, 10, 2)
            elif state=="W":
                cv2.drawMarker(outputImg, (p[0],p[1]), (255, 0, 0), cv2.MARKER_TILTED_CROSS, 10, 2)
            elif state=="N":
                cv2.drawMarker(outputImg, (p[0],p[1]), (0, 255, 0), cv2.MARKER_CROSS, 10)
            j += 1
        i += 1
    return outputImg


# 仕組みはdrawTerritoryColorと同様。compareの内容に応じて画像上に点を付与する。
def drawCompareStone(img,territoryTable):
    outputImg = img.copy()
    crossPoints = retCrossPoints(img)
    i = 0
    for p_row in crossPoints:
        j = 0
        for p in p_row:
            state = territoryTable[i][j]
            if str(state)=="False":
                cv2.drawMarker(outputImg, (p[0],p[1]), (0, 255, 0), cv2.MARKER_TILTED_CROSS, 10, 2)
            j += 1
        i += 1
    return outputImg

#           --- 処理開始 ---

img_A = cv2.imread("./A.png")
img_B = cv2.imread("./B.png")

# 交点付与
PTS_A = drawCrossPoints(img_A)
cv2.imshow("PTS_A",PTS_A)
cv2.waitKey(0)

PTS_B = drawCrossPoints(img_B)
cv2.imshow("PTS_B",PTS_B)
cv2.waitKey(0)

# resに点を付与
RES_A = drawXP_Rect(PTS_A)
cv2.imshow("RES_A",RES_A)
cv2.waitKey(0)

RES_B = drawXP_Rect(PTS_B)
cv2.imshow("RES_B",RES_B)
cv2.waitKey(0)


stonePosition_A = checkStonePosition(RES_A)
stonePosition_B = checkStonePosition(RES_B)
# print(re.sub("[|[[|]|]|],", "", str(stonePosition).replace("], [","], \n[")))
# stonePosition の情報を.csvに保存
# with open('./Results/stonePosition.csv', 'w', newline="") as f:
#     writer = csv.writer(f)
#     writer.writerows(stonePosition)

# print("stonePosition: \n" + str(stonePosition).replace("], [","], \n[") + "\n")

# 結果
RESULT_A = drawTerritoryColor(img_A,stonePosition_A)
cv2.imshow("RESULT_A",RESULT_A)
cv2.waitKey(0)

RESULT_B = drawTerritoryColor(img_B,stonePosition_B)
cv2.imshow("RESULT_B",RESULT_B)
cv2.waitKey(0)


print("END")

'''
# 偽の碁盤情報を用意、stonePositionと比較
dummy = [
[N, B, B, W, W, N, N, N, N, N, N, N, N, N, W, W, W, W, B], 
[N, B, W, W, N, W, N, N, N, N, N, W, W, N, W, B, W, B, B], 
[N, B, W, B, W, W, N, N, N, W, W, B, W, W, B, B, B, B, N], 
[N, N, B, B, B, W, W, W, W, B, B, B, W, B, B, B, B, N, N], 
[N, N, B, W, W, B, B, B, B, B, N, B, W, B, W, W, B, N, N], 
[N, N, B, W, W, W, B, W, B, W, B, N, B, B, W, W, B, N, N], 
[N, N, N, B, B, W, W, W, W, W, B, B, W, W, W, B, N, N, N], 
[N, N, B, B, W, N, W, B, B, B, B, B, W, B, W, B, B, B, B], 
[N, N, B, W, W, N, W, B, B, W, W, B, W, B, W, W, B, W, B], 
[N, B, W, N, N, N, W, W, B, B, W, B, B, B, B, W, B, W, W], 
[N, B, W, N, N, N, W, B, B, B, W, W, W, W, W, B, N, W, N], 
[B, B, W, N, N, W, B, B, W, W, N, N, N, N, N, N, W, N, N], 
[W, B, W, W, W, W, W, W, W, B, N, N, N, N, N, W, B, W, W], 
[W, W, W, B, B, B, W, B, B, W, W, N, N, N, N, W, B, W, W], 
[N, W, B, B, B, B, B, N, B, W, W, N, N, N, W, B, B, B, W], 
[W, W, W, W, W, B, N, B, N, B, B, W, W, W, W, W, B, B, W], 
[B, W, B, W, W, B, N, W, B, B, B, W, B, B, W, W, W, B, B], 
[B, B, B, B, B, N, N, N, N, N, B, B, N, B, B, W, B, B, N], 
[N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, B, N, N, N]]

compare = np.array(stonePosition) == np.array(dummy)
resultDummyCompare = drawCompareStone(boardImg, compare)
cv2.imshow("compare", resultDummyCompare)
cv2.waitKey(0)
'''