import cv2
import numpy as np
import matplotlib.pyplot as plt
import re
import csv
import os
if os.name == 'nt': os.system('cls')
else : os.system("clear")


#           --- 関数の定義 ---

# 透視変換を行う
def perspectiveTransform(img, pts_input, pts_output):   # (画像，オリジナルにおける四隅の座標，変換後の四隅の座標)
    # "img.shape"：画像の情報。「高さ・幅・チャンネル数」を返す
    raws, cols, ch = img.shape  # img.shapeで得た情報を順番にraws,cols,ch変数に格納
    # cv2.getPerspectiveTransform()：透視写像行列を計算する
    M = cv2.getPerspectiveTransform(pts_input, pts_output)  # M=透視写像行列
    # cv.warpPerspective()：透視変換
    outputImg = cv2.warpPerspective(img, M, (800, 800)) # outputImg=変換を行った画像
    return outputImg

# 点→多角形表示。碁盤を切り抜く四点を繋いだ四角形の可視化用。
def drawCorner(img,pts):
    outputImg = img.copy()
    cv2.polylines(outputImg, [pts], True, (0,255,0), thickness=5, lineType=cv2.LINE_AA)
    return outputImg

# ノイズ処理を行う
def reduceNoise(img, medianBoxSize, kernelSize):
    # cv2.medianBlur()：メディアンフィルタ
    cv2.medianBlur(img, medianBoxSize)
    # np.ones(サイズ，データ型)：全要素が1の行列を生成。この場合kernelSize*kernelSizeの、全要素が1の行列が用意される。
    kernel = np.ones((kernelSize, kernelSize), np.uint8)    #np.uint8：NumPyのデータ型のひとつ、符号なし8bit
    # cv2.morphologyEx(画像，処理，構造要素)：“モルフォロジー”（画像上の図形に対して作用するシンプルな処理）関数
        # cv2.MORPH_CLOSE：クロージング処理
    outputImg = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    return outputImg

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

""" たぶん不要な処理たち

def addStateToNeighbourhood(state, neighbourhood):
    isAdded = False
    if state<11 and state>=B:
        neighbourhood.append(B)
        isAdded = True
    elif state>244:
        neighbourhood.append(W)
        isAdded = True
    return [neighbourhood, isAdded]

def checkTeritory(point,territoryTable):
    x, y = point[:]
    neighbourhood = []
    
    # 周りの確定済みの状態を近傍リストに追加
    # 左上
    if x>B and y>B:
        leftUpperState = territoryTable[xN][yN]
        neighbourhood = addStateToNeighbourhood(leftUpperState, neighbourhood)[B]
    # 上
    if x>B:
        upperState = territoryTable[xN][y]
        neighbourhood = addStateToNeighbourhood(upperState,neighbourhood)[B]
    # 右上
    if x>B and y+1<19:
        rightUpperState = territoryTable[xN][y+1]
        neighbourhood = addStateToNeighbourhood(rightUpperState,neighbourhood)[B]
    # 左
    if y>B:
        leftState = territoryTable[x][yN]
        neighbourhood = addStateToNeighbourhood(leftState,neighbourhood)[B]

    # 残りの状態を石に当たるまで走査
    # 右
    j = 1
    while y+j<19:
        rightState = territoryTable[x][y+j]
        neighbourhood,flag = addStateToNeighbourhood(rightState,neighbourhood)[:]
        if flag:
            break
        else:
            j += 1
    # 左下
    i = 1
    j = 1
    while x+i<19 and y-j>=B:
        leftButtomState = territoryTable[x+i][y-j]
        neighbourhood,flag = addStateToNeighbourhood(leftButtomState,neighbourhood)[:]
        if flag:
            break
        else:
            i += 1
            j += 1
    # 下
    i = 1
    while x+i<19:
        buttomState = territoryTable[x+i][y]
        neighbourhood,flag = addStateToNeighbourhood(buttomState,neighbourhood)[:]
        if flag:
            break
        else:
            i += 1
    # 右下
    i = 1
    j = 1
    while x+i<19 and y+j<19:
        rightButtomState = territoryTable[x+i][y+j]
        neighbourhood,flag = addStateToNeighbourhood(rightButtomState,neighbourhood)[:]
        if flag:
            break
        else:
            i += 1
            j += 1

    # 近傍のリストのどちらが多いか
    if neighbourhood.count(B) > neighbourhood.count(W):
        targetState = 1B
    else:
        targetState = 245

    territoryTable[x][y] = targetState
    return territoryTable

def makeTerritoryTable(stonePosition):
    territoryTable = stonePosition.copy()
    for x in range(19):
        for y in range(19):
            if territoryTable[x][y]==N:
                point = [x,y]
                territoryTable = checkTeritory(point,territoryTable)            
    return territoryTable

"""
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

# ファイル指定と、指定ファイルの表示
filename = './Input_IMG/IMG_5604.jpg'
originalImg = cv2.imread(filename)
cv2.namedWindow("originalImg", cv2.WINDOW_NORMAL)   # 画像がデカすぎるので縮小表示用
cv2.imshow("originalImg",originalImg)
cv2.waitKey(0)

# 座標指定：[左上],[右上],[右下],[左下]
pts = np.array([[801,503],[2617,156],[2810,2212],[789,2152]], np.int32)
cornerOfGoBoard = np.float32(pts) # float32に型変換。透視変換行列の計算で必要になる。
cornerOfImage = np.float32([[0,0], [800,0], [800,800], [0, 800]])

# 切り抜き領域可視化
cornerImg=drawCorner(originalImg,pts)
for p in pts:
    cv2.drawMarker(cornerImg, (p[0],p[1]), (0, 255, 0), cv2.MARKER_TILTED_CROSS, 50, 10)
cv2.namedWindow("cornerImg", cv2.WINDOW_NORMAL)
cv2.imshow("cornerImg",cornerImg)
cv2.waitKey(0)
cv2.imwrite('./Results/cornerImg.png', cornerImg)

# 透視変換(Perspective Transform)
boardImg = perspectiveTransform(originalImg, cornerOfGoBoard, cornerOfImage)
cv2.imshow("Results/boardImg",boardImg)
cv2.waitKey(0)
cv2.imwrite('./Results/boardImg.png', boardImg)

# 交点付与
boardWithPointsImg = drawCrossPoints(boardImg)
cv2.imshow("boardWithPointsImg",boardWithPointsImg)
cv2.waitKey(0)
cv2.imwrite('./Results/boardWithPointsImg.png', boardWithPointsImg)

# ノイズ処理
noiseReducedImg = reduceNoise(boardImg, 27, 25)
cv2.imshow("noiseReducedImg",noiseReducedImg)
cv2.waitKey(0)
cv2.imwrite('./Results/noiseReducedImg.png', noiseReducedImg)

# 確認用の表示(BGR→HSV変換)
hsvImg = cv2.cvtColor(noiseReducedImg, cv2.COLOR_BGR2HSV)
cv2.imshow("hsvImg",hsvImg)
cv2.waitKey(0)
cv2.imwrite('./Results/hsvImg.png', hsvImg)

#マスク
# beige = np.uint8([[[61,91,146]]])                   # これ使われてない
# hsv_beige = cv2.cvtColor(beige,cv2.COLOR_BGR2HSV)   # これ使われてない……
lower_beige = np.array([10,50,50])      # 閾値の下限
upper_beige = np.array([30,255,255])    # 閾値の上限

mask_beige = cv2.inRange(hsvImg, lower_beige, upper_beige)
cv2.imshow("mask_beige",mask_beige)
cv2.waitKey(0)
cv2.imwrite('./Results/mask_beige.png', mask_beige)

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