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

print("START")

# 処理開始
# A
img_A = cv2.imread("DSC_0041.jpg", cv2.IMREAD_GRAYSCALE)

# 座標指定：[左上],[右上],[右下],[左下]
pts_A = np.array([[1126,250],[2735,105],[2745,1823],[1103,1716]], np.int32)
cornerOfGoBoard_A = np.float32(pts_A) # float32に型変換。透視変換行列の計算で必要になる。
cornerOfImage_A = np.float32([[0,0], [800,0], [800,800], [0, 800]])

# 透視変換(Perspective Transform)
boardImg_A = perspectiveTransform(img_A, cornerOfGoBoard_A, cornerOfImage_A)
cv2.imshow("A",boardImg_A)
cv2.waitKey(0)

# B
img_B = cv2.imread("DSC_0042.jpg", cv2.IMREAD_GRAYSCALE)

# 座標指定：[左上],[右上],[右下],[左下]
pts_B = np.array([[1288,339],[2604,128],[2542,1863],[1205,1634]], np.int32)
cornerOfGoBoard_B = np.float32(pts_B) # float32に型変換。透視変換行列の計算で必要になる。
cornerOfImage_B = np.float32([[0,0], [800,0], [800,800], [0, 800]])

# 透視変換(Perspective Transform)
boardImg_B = perspectiveTransform(img_B, cornerOfGoBoard_B, cornerOfImage_B)
cv2.imshow("B",boardImg_B)
cv2.waitKey(0)

# ポスタリゼーション
x = np.arange(256)
n = 3  # 画素値を何段階で表現するか
bins = np.linspace(0, 255, n + 1)
y = np.array([bins[i - 1] for i in np.digitize(x, bins)]).astype(int)

img_MEDIAN_A = cv2.medianBlur(boardImg_A, 29)
cv2.imshow("img_MEDIAN_A",img_MEDIAN_A)
cv2.waitKey(0)

img_MEDIAN_B = cv2.medianBlur(boardImg_B, 29)
cv2.imshow("img_MEDIAN_B",img_MEDIAN_B)
cv2.waitKey(0)

# 変換する。
dst_A = cv2.LUT(img_MEDIAN_A, y)
dst_B = cv2.LUT(img_MEDIAN_B, y)

cv2.imwrite("A.png",dst_A)
cv2.imwrite("B.png",dst_B)

#画像の表示
# plt.gray() # 表示カラーマップをグレースケールとする(*)
# plt.imshow(dst_A)
# plt.savefig("A.png")

# plt.imshow(dst_B)
# plt.savefig("B.png")

print("END")