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
print("Input filename...")
filename = str(input()) # ファイル名指定
print("\n")

print("Input threshold_black (default=58)...")
threshold_black = str(input())
if(len(threshold_black)==0):
    threshold_black=58
else:
    threshold_black=int(threshold_black)
print(threshold_black)

print("Input threshold_white (default=158)...")
threshold_white = str(input())
if(len(threshold_white)==0):
    threshold_white=158
else:
    threshold_white=int(threshold_white)
print(threshold_white)

# print("Threshold_black = " + str(threshold_black))







if not(os.path.exists("./Results/"+filename)): os.makedirs("./Results/"+filename)   # ファイル名のディレクトリを作る（画像ごとにいちいち座標とか再設定するのが面倒になった）
originalImg = cv2.imread("./Input_IMG/"+filename+".jpg")

# 画像名のディレクトリにあるptlist.txtをもとに切り抜く四隅を指定（座標指定：[左上],[右上],[右下],[左下]）
ptlist=[]
if not(os.path.exists('./Results/'+filename+'/ptlist.txt')): 
    path = './Results/'+filename+'/ptlist.txt'
    f = open(path, 'w')
    f.write('')  # 何も書き込まなくてファイルは作成されました
    f.close()
    print("WARNING: ./Results/"+filename+"/ptlist.txt generated.")
    quit()

for l in open('./Results/'+filename+'/ptlist.txt').readlines():
    data = l[:-1].split(',')
    ptlist += [[int(data[0]),int(data[1])]]

pts = np.array(ptlist, np.int32)
cornerOfGoBoard = np.float32(pts) # float32に型変換。透視変換行列の計算で必要になる。
cornerOfImage = np.float32([[0,0], [800,0], [800,800], [0, 800]])

# 切り抜き領域可視化
cornerImg = MOD.drawCorner(originalImg,pts)
for p in pts:
    cv2.drawMarker(cornerImg, (p[0],p[1]), (0, 255, 0), cv2.MARKER_TILTED_CROSS, 50, 10)
# cv2.namedWindow("cornerImg", cv2.WINDOW_NORMAL)
# cv2.imshow("cornerImg",cornerImg)
# cv2.waitKey(0)
cv2.imwrite('./Results/' + filename + '/cornerImg.jpg', cornerImg)

# 透視変換(Perspective Transform)
boardImg = MOD.perspectiveTransform(originalImg, cornerOfGoBoard, cornerOfImage)
# cv2.imshow("Results/boardImg",boardImg)
# cv2.waitKey(0)
cv2.imwrite('./Results/' + filename + '/boardImg.jpg', boardImg)

# BGR→GRAY変換
GRAYImg = cv2.cvtColor(boardImg, cv2.COLOR_BGR2GRAY)
# cv2.imshow("GRAYImg",GRAYImg)
# cv2.waitKey(0)
cv2.imwrite('./Results/' + filename + '/GRAYImg.jpg', GRAYImg)


kernelSize = 35
median = cv2.medianBlur(GRAYImg,kernelSize)
cv2.imwrite('./Results/' + filename + '/median.jpg', median)
blur = cv2.blur(GRAYImg,(kernelSize,kernelSize))
cv2.imwrite('./Results/' + filename + '/blur.jpg', blur)

# ノイズ処理

noiseReducedImg = cv2.medianBlur(GRAYImg,kernelSize)
# noiseReducedImg = cv2.blur(GRAYImg,(kernelSize,kernelSize))
# cv2.imshow("noiseReducedImg",noiseReducedImg)
# cv2.waitKey(0)
cv2.imwrite('./Results/' + filename + '/noiseReducedImg.jpg', noiseReducedImg)

# 結果に重ねる用の，カラー画像に変換したnoiseReducedImg(GRAY)
GRAY_to_COLOR_noiseReduced = cv2.cvtColor(noiseReducedImg, cv2.COLOR_GRAY2BGR)
GRAY_to_COLOR = cv2.cvtColor(GRAYImg,cv2.COLOR_GRAY2BGR)


# 交点付与（これ自体はなくてもいいが，取得領域の確認用）
boardWithAreaImg = MOD.drawXP_Rect(GRAY_to_COLOR_noiseReduced)
# cv2.imshow("boardWithAreaImg",boardWithAreaImg)
# cv2.waitKey(0)
cv2.imwrite('./Results/' + filename + '/boardWithAreaImg.jpg', boardWithAreaImg)

color_boardWithAreaImg = MOD.drawXP_Rect(boardImg)
# cv2.imshow("color_boardWithAreaImg",color_boardWithAreaImg)
# cv2.waitKey(0)
cv2.imwrite('./Results/' + filename + '/color_boardWithAreaImg.jpg', color_boardWithAreaImg)

# 石の有無を計算
stonePosition_NoMask = MOD.checkStonePosition(noiseReducedImg, threshold_black, threshold_white) 
stonePosition_NoMask_ALT = MOD.checkStonePosition_ALT(noiseReducedImg, threshold_black, threshold_white) 
# noiseReducedに重ねて計算結果を表示
result_noiseReduced = MOD.drawTerritoryColor(GRAY_to_COLOR_noiseReduced,stonePosition_NoMask)
# cv2.imshow("result_noiseReduced",result_noiseReduced)
# cv2.waitKey(0)
cv2.imwrite('./Results/' + filename + '/result_noiseReduced.jpg', result_noiseReduced)

# 盤面画像に重ねて計算結果を表示
result = MOD.drawTerritoryColor(GRAY_to_COLOR,stonePosition_NoMask)
# cv2.imshow("result",result)
# cv2.waitKey(0)
cv2.imwrite('./Results/' + filename + '/result.jpg', result)

#! 白のしきい値が拾ってる範囲を図に
inRange_WHITE = cv2.inRange(noiseReducedImg,threshold_white,255)
# cv2.imshow("inRange_WHITE",inRange_WHITE)
# cv2.waitKey(0)
# cv2.imwrite('./Results/' + filename + '/inRange_WHITE.jpg', inRange_WHITE)

# 結果
# resultImg = MOD.drawTerritoryColor(GRAY_to_COLOR,stonePosition)
# cv2.imshow("resultImg",resultImg)
# cv2.waitKey(0)
# cv2.imwrite('./Results/' + filename + '/resultIMG.jpg', resultImg)

if not(os.path.exists('./Results/' + filename + '/stonePosition.csv')): 
    path = './Results/' + filename + '/stonePosition.csv'
    f = open(path, 'w')
    f.write('')  # 何も書き込まなくてファイルは作成されました
    f.close()
    print("WARNING: ./Results/" + filename + '/stonePosition.csv generated!')

if not(os.path.exists('./Results/' + filename + '/' + filename + '.csv')): 
    path = './Results/' + filename + '/' + filename + '.csv'
    f = open(path, 'w')
    f.write('')  # 何も書き込まなくてファイルは作成されました
    f.close()
    print("WARNING: ./Results/" + filename + '/' + filename + '.csv generated!')


with open('./Results/' + filename + '/stonePosition.csv', 'w', newline="") as file: # CSVに書き込み
    writer = csv.writer(file, lineterminator='\n')
    writer.writerows(stonePosition_NoMask)

with open('./Results/' + filename + '/stonePosition_ALT.csv', 'w', newline="") as file: # CSVに書き込み
    writer = csv.writer(file, lineterminator='\n')
    writer.writerows(stonePosition_NoMask_ALT)



    # ファイル名.csvに，正常な碁石の配置を記録しておくことで，一致した確率が求められる．
with open('./Results/' + filename + '/' + filename + '.csv', 'r', newline="") as f: # 偽の碁盤情報をdummyPosition.csvから取得，比較を行う
    reader = csv.reader(f) 
    l = [row for row in reader]
    # ndarrayを比較演算子で比較すると，各要素に対して一致してるかどうかの真理値を返す．

    # csv上の石の数
    BLACK_c = 0
    WHITE_c = 0
    BLACK_d = 0
    WHITE_d = 0

    for R_csv in l: 
        BLACK_c += R_csv.count('B')
        WHITE_c += R_csv.count('W')

    # システムが検知(detect)した石の検知数
    for R_detected in stonePosition_NoMask:
        BLACK_d += R_detected.count('B')
        WHITE_d += R_detected.count('W')

    # # 比較結果を画像に重ねる．
    compare = np.array(stonePosition_NoMask) == np.array(l)
    # print(compare)
    resultCompare = MOD.drawCompareStone(boardImg, compare)
    # cv2.imshow("compare", resultCompare)
    # cv2.waitKey(0)
    cv2.imwrite('./Results/' + filename + '/resultCompare.jpg', resultCompare)

kernel_high_pass = np.array([
                            [-1, -1, -1],
                            [-1,  8, -1],
                            [-1, -1, -1]
                            ], np.float32)

img_high_pass = cv2.filter2D(GRAYImg, -1, kernel_high_pass)
cv2.imwrite('./Results/' + filename + '/HighPass.jpg', img_high_pass)

cimg = cv2.cvtColor(inRange_WHITE,cv2.COLOR_GRAY2BGR)

circles = cv2.HoughCircles(inRange_WHITE,cv2.HOUGH_GRADIENT,1,20,
                            param1=50,param2=30,minRadius=0,maxRadius=300)

circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

cv2.imwrite('./Results/' + filename + '/detected circles.jpg',cimg)

ret, img_otsu = cv2.threshold(GRAYImg, 0, 255, cv2.THRESH_OTSU)
cv2.imwrite('./Results/' + filename + '/img_otsu.jpg',img_otsu)

print(ret)


print("END")
