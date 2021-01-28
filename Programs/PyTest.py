# 本当にこんなにインポートする必要があるのかは分からない．減らせるかもしれない．
import cv2
import numpy as np
import matplotlib.pyplot as plt
import re
import csv
import Module as MOD    # 関数部分を1つのファイルに分けた．使い回せるように．
# OSに限らず，この下の3行で実行時にコンソール内容を消去する．clearとかclsとかの実行が面倒なので。
import os   
if os.name == 'nt': os.system('cls')
else : os.system("clear")

#           --- 処理開始 ---

#? ファイル指定
print("Input filename...")
filename = str(input()) # 入力input()を文字列変換し、filenameに格納

if not(os.path.isfile("../RawData/Input_IMG/"+filename+".jpg")):
    print("file not found.")
    print("Program terminated.")
    quit()


if not(os.path.exists("../RawData/Results/"+filename)): # もしファイル名のフォルダが無い場合
    os.makedirs("../RawData/Results/"+filename)   # ファイル名のディレクトリを作る（画像ごとにいちいち座標とか再設定するのが面倒になった）
    print("WARNING: ../RawData/Results/"+filename+"/ generated.")

if not(os.path.exists('../RawData/Results/'+filename+'/ptlist.txt')): # もしptlist.txtが作成されていない場合
    path = '../RawData/Results/'+filename+'/ptlist.txt'
    f = open(path, 'w')
    f.write('')  # ptlist.txtに何も書き込まない（空のptlist.txtを作成する）
    f.close()
    print("WARNING: ../RawData/Results/"+filename+"/ptlist.txt generated.")
    print("Program terminated.")
    quit()


def_black = 52
def_white = 158

print("Input threshold_black (default="+str(def_black)+")...")
threshold_black = str(input())
if(len(threshold_black)==0):
    threshold_black=def_black
else:
    threshold_black=int(threshold_black)

print("Input threshold_white (default="+str(def_white)+")...")
threshold_white = str(input())
if(len(threshold_white)==0):
    threshold_white=def_white
else:
    threshold_white=int(threshold_white)


#? 指定した画像の情報を、変数originalImgに代入
originalImg = cv2.imread("../RawData/Input_IMG/"+filename+".jpg")

#? 画像名のディレクトリにあるptlist.txtをもとに切り抜く四隅を指定（座標指定：[左上],[右上],[右下],[左下]）
ptlist=[]
for l in open('../RawData/Results/'+filename+'/ptlist.txt').readlines():
    data = l[:-1].split(',')
    ptlist += [[int(data[0]),int(data[1])]]

pts = np.array(ptlist, np.int32)
cornerOfGoBoard = np.float32(pts) # float32に型変換。透視変換行列の計算で必要になる。
cornerOfImage = np.float32([[0,0], [800,0], [800,800], [0, 800]]) # 変換後の四角形の形指定。この場合800x800pxの正方形

#? 切り抜き領域可視化
cornerImg = MOD.drawCorner(originalImg,pts)
for p in pts:
    cv2.drawMarker(cornerImg, (p[0],p[1]), (0, 255, 0), cv2.MARKER_TILTED_CROSS, 50, 10)
# cv2.namedWindow("cornerImg", cv2.WINDOW_NORMAL) # リサイズ可能ウィンドウの生成。元画像はサイズが大きすぎるので。
# cv2.imshow("cornerImg",cornerImg)
# cv2.waitKey(0)
cv2.imwrite('../RawData/Results/' + filename + '/cornerImg.jpg', cornerImg)

#? 透視変換(Perspective Transform)
boardImg = MOD.perspectiveTransform(originalImg, cornerOfGoBoard, cornerOfImage)
# cv2.imshow("Results/boardImg",boardImg)
# cv2.waitKey(0)
cv2.imwrite('../RawData/Results/' + filename + '/boardImg.jpg', boardImg)

#? BGR→GRAY変換
GRAYImg = cv2.cvtColor(boardImg, cv2.COLOR_BGR2GRAY)
# cv2.imshow("GRAYImg",GRAYImg)
# cv2.waitKey(0)
cv2.imwrite('../RawData/Results/' + filename + '/GRAYImg.jpg', GRAYImg)


#? フィルタのサイズ
    #! メディアンフィルタの際は、カーネルサイズは奇数でないとエラーが出る（偶数だと中央値が1つに決まらないため）。
kernelSize = 35 

#? 同じカーネルサイズでの、メディアンフィルタ適用画像（median）と平均化フィルタ適用画像（blur）を生成。
    #! 確認用。後ろの処理で使ってないから、消してもいい。
# median = cv2.medianBlur(GRAYImg,kernelSize)
# cv2.imwrite('../RawData/Results/' + filename + '/median.jpg', median)
# blur = cv2.blur(GRAYImg,(kernelSize,kernelSize))
# cv2.imwrite('../RawData/Results/' + filename + '/blur.jpg', blur)



#? ノイズ処理
noiseReducedImg = cv2.medianBlur(GRAYImg,kernelSize) # この場合、メディアンフィルタを適用しただけ。上のmedianと同じものが出来上がる。
# noiseReducedImg = cv2.blur(GRAYImg,(kernelSize,kernelSize))
# cv2.imshow("noiseReducedImg",noiseReducedImg)
# cv2.waitKey(0)
cv2.imwrite('../RawData/Results/' + filename + '/noiseReducedImg.jpg', noiseReducedImg)


#? グレースケール画像に色付きのマーカーを付与しても白黒表示になってしまうため、再度カラー画像に変換。
    #! 結果表示で使うだけだから、なくてもいい。
GRAY_to_COLOR_noiseReduced = cv2.cvtColor(noiseReducedImg, cv2.COLOR_GRAY2BGR)
GRAY_to_COLOR = cv2.cvtColor(GRAYImg,cv2.COLOR_GRAY2BGR)


#? ノイズ処理画像に交点付与（取得領域の確認用）
boardWithAreaImg = MOD.drawXP_Rect(GRAY_to_COLOR_noiseReduced)
# cv2.imshow("boardWithAreaImg",boardWithAreaImg)
# cv2.waitKey(0)
cv2.imwrite('../RawData/Results/' + filename + '/boardWithAreaImg.jpg', boardWithAreaImg)

#? 射影変換後の正方形画像に交点付与（取得領域の確認用）
color_boardWithAreaImg = MOD.drawXP_Rect(boardImg)
# cv2.imshow("color_boardWithAreaImg",color_boardWithAreaImg)
# cv2.waitKey(0)
cv2.imwrite('../RawData/Results/' + filename + '/color_boardWithAreaImg.jpg', color_boardWithAreaImg)

#? 石の有無を計算
stonePosition_NoMask = MOD.checkStonePosition(noiseReducedImg, threshold_black, threshold_white) 
stonePosition_NoMask_ALT = MOD.checkStonePosition_ALT(noiseReducedImg, threshold_black, threshold_white) 

#? noiseReducedに重ねて計算結果を表示
result_noiseReduced = MOD.drawTerritoryColor(GRAY_to_COLOR_noiseReduced,stonePosition_NoMask)
# cv2.imshow("result_noiseReduced",result_noiseReduced)
# cv2.waitKey(0)
cv2.imwrite('../RawData/Results/' + filename + '/result_noiseReduced.jpg', result_noiseReduced)

#? boardImg(グレー)に重ねて計算結果を表示
result = MOD.drawTerritoryColor(GRAY_to_COLOR,stonePosition_NoMask)
# cv2.imshow("result",result)
# cv2.waitKey(0)
cv2.imwrite('../RawData/Results/' + filename + '/result.jpg', result)

#! 白のしきい値が拾ってる範囲を示した画像。論文用に作っただけ
# inRange_WHITE = cv2.inRange(noiseReducedImg,threshold_white,255)
# cv2.imshow("inRange_WHITE",inRange_WHITE)
# cv2.waitKey(0)
# cv2.imwrite('../RawData/Results/' + filename + '/inRange_WHITE.jpg', inRange_WHITE)

# 結果
# resultImg = MOD.drawTerritoryColor(GRAY_to_COLOR,stonePosition)
# cv2.imshow("resultImg",resultImg)
# cv2.waitKey(0)
# cv2.imwrite('../RawData/Results/' + filename + '/resultIMG.jpg', resultImg)


#? 結果をCSVに書き込み。上2つのif文は、csvファイルが無かったら作成する処理。
if not(os.path.exists('../RawData/Results/' + filename + '/stonePosition.csv')): 
    path = '../RawData/Results/' + filename + '/stonePosition.csv'
    f = open(path, 'w')
    f.write('')  # 何も書き込まなくてファイルは作成されました
    f.close()
    print("WARNING: ../RawData/Results/" + filename + '/stonePosition.csv generated!')

if not(os.path.exists('../RawData/Results/' + filename + '/' + filename + '.csv')): 
    path = '../RawData/Results/' + filename + '/' + filename + '.csv'
    f = open(path, 'w')
    f.write('')  # 何も書き込まなくてファイルは作成されました
    f.close()
    print("WARNING: ../RawData/Results/" + filename + '/' + filename + '.csv generated!')


with open('../RawData/Results/' + filename + '/stonePosition.csv', 'w', newline="") as file: # CSVに書き込み
    writer = csv.writer(file, lineterminator='\n')
    writer.writerows(stonePosition_NoMask)

with open('../RawData/Results/' + filename + '/stonePosition_ALT.csv', 'w', newline="") as file: # CSVに書き込み
    writer = csv.writer(file, lineterminator='\n')
    writer.writerows(stonePosition_NoMask_ALT)


    #! 処理とは関係ない。結果を数える用の処理。
#     # ファイル名.csvに，正常な碁石の配置を記録しておくことで，一致した確率が求められる．
# with open('../RawData/Results/' + filename + '/' + filename + '.csv', 'r', newline="") as f: # 偽の碁盤情報をdummyPosition.csvから取得，比較を行う
#     reader = csv.reader(f) 
#     l = [row for row in reader]
#     # ndarrayを比較演算子で比較すると，各要素に対して一致してるかどうかの真理値を返す．

#     # csv上の石の数
#     BLACK_c = 0
#     WHITE_c = 0
#     BLACK_d = 0
#     WHITE_d = 0

#     for R_csv in l: 
#         BLACK_c += R_csv.count('B')
#         WHITE_c += R_csv.count('W')

#     # システムが検知(detect)した石の検知数
#     for R_detected in stonePosition_NoMask:
#         BLACK_d += R_detected.count('B')
#         WHITE_d += R_detected.count('W')

#     # # 比較結果を画像に重ねる．
#     compare = np.array(stonePosition_NoMask) == np.array(l)
#     # print(compare)
#     resultCompare = MOD.drawCompareStone(boardImg, compare)
#     # cv2.imshow("compare", resultCompare)
#     # cv2.waitKey(0)
#     cv2.imwrite('../RawData/Results/' + filename + '/resultCompare.jpg', resultCompare)

print("END")
