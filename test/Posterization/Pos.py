import cv2
import numpy as np
import matplotlib.pyplot as plt

import os
if os.name == 'nt': os.system('cls')
else : os.system("clear")

# 透視変換を行う
def perspectiveTransform(img, pts_input, pts_output):   # (画像，オリジナルにおける四隅の座標，変換後の四隅の座標)
    # "img.shape"：画像の情報。「高さ・幅・チャンネル数」を返す
    raws, cols = img.shape  # img.shapeで得た情報を順番にraws,cols,ch変数に格納
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

print("START")

# 処理開始

img = cv2.imread("DSC_0041.jpg", cv2.IMREAD_GRAYSCALE)
# img = cv2.imread("20201025225242_1.jpg", cv2.IMREAD_GRAYSCALE)
cv2.imshow("img",img)
cv2.waitKey(0)

# 座標指定：[左上],[右上],[右下],[左下]
pts = np.array([[1126,250],[2735,105],[2745,1823],[1103,1716]], np.int32)
cornerOfGoBoard = np.float32(pts) # float32に型変換。透視変換行列の計算で必要になる。
cornerOfImage = np.float32([[0,0], [800,0], [800,800], [0, 800]])

# 切り抜き領域可視化
cornerImg=drawCorner(img,pts)
for p in pts:
    cv2.drawMarker(cornerImg, (p[0],p[1]), (0, 255, 0), cv2.MARKER_TILTED_CROSS, 50, 10)
cv2.namedWindow("cornerImg", cv2.WINDOW_NORMAL)
cv2.imshow("cornerImg",cornerImg)
cv2.waitKey(0)

# 透視変換(Perspective Transform)
boardImg = perspectiveTransform(img, cornerOfGoBoard, cornerOfImage)
cv2.imshow("Results/boardImg",boardImg)
cv2.waitKey(0)

# ポスタリゼーション
x = np.arange(256)
n = 3  # 画素値を何段階で表現するか
bins = np.linspace(0, 255, n + 1)
y = np.array([bins[i - 1] for i in np.digitize(x, bins)]).astype(int)

img_MEDIAN = cv2.medianBlur(boardImg, 29)
cv2.imshow("img_MEDIAN",img_MEDIAN)
cv2.waitKey(0)

# 変換する。
dst = cv2.LUT(img_MEDIAN, y)

#画像の表示
plt.gray() # 表示カラーマップをグレースケールとする(*)
plt.imshow(dst)
plt.show()


# plot_grayscale_conversion(img, dst)
print("END")