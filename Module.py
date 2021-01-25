# ソースコードを見やすく，機能を使い回せるように，関数部分をモジュール化したい．
import cv2
import numpy as np
import matplotlib.pyplot as plt

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
    cv2.blur(img, medianBoxSize)
    # np.ones(サイズ，データ型)：全要素が1の行列を生成。この場合kernelSize*kernelSizeの、全要素が1の行列が用意される。
    # kernel = np.ones((kernelSize, kernelSize), np.uint8)    #np.uint8：NumPyのデータ型のひとつ、符号なし8bit
    # cv2.morphologyEx(画像，処理，構造要素)：“モルフォロジー”（画像上の図形に対して作用するシンプルな処理）関数
        # cv2.MORPH_CLOSE：クロージング処理
    # outputImg = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
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
                x += 4   # i=Bのとき、x座標+7    （端だけ交点をずらす）
            if j==0:
                y += 4   # jも同様
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
            cv2.rectangle(outputImg, (p[0]-8,p[1]-8),(p[0]+20,p[1]+20),(0,255,0),1)

    return outputImg


# 石の位置・種類の判別
def checkStonePosition(img, threshold_black, threshold_white):
    crossPoints = retCrossPoints(img)
    conditionOfBoard = []
    none = 10.0

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
            if colorAve < none: # 明るさ平均がnone（上で宣言）以下→"N"を付与
                condition_row.append("N")
            elif colorAve < threshold_black: # 明るさ平均がblackStone（上で宣言）以下→"B"を付与
                condition_row.append("B")
            elif colorAve > threshold_white:
                condition_row.append("W") # 明るさ平均がwhiteStone（上で宣言）以下→"W"を付与
            else:
                condition_row.append("U")
        conditionOfBoard.append(condition_row)

    # これに石の情報があった！！
    # print(conditionOfBoard)
    return conditionOfBoard

def checkStonePosition_ALT(img, threshold_black, threshold_white):
    crossPoints = retCrossPoints(img)
    conditionOfBoard = []

    for p_row in crossPoints:
        condition_row = []
        for p in p_row:
            rect = img[p[1]-3:p[1]+7, p[0]-3:p[0]+7]

            # rect（=緑枠内の全ピクセルのBGR）の平均値を取得
            colorAve = np.average(rect)
            condition_row.append(colorAve)
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
            else:
                cv2.drawMarker(outputImg, (p[0],p[1]), (0, 255, 255), cv2.MARKER_CROSS, 10)
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

def list_difference(list1, list2):
    result = list1.copy()
    for value in list2:
        if value in result:
            result.remove(value)

    return result