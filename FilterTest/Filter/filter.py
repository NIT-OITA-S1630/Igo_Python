import cv2
import numpy as np
import os
if os.name == 'nt': os.system('cls')
else : os.system("clear")

# ノイズ処理を行う
# def reduceNoise(img, medianBoxSize, kernelSize):
#     # cv2.medianBlur()：メディアンフィルタ
#     cv2.medianBlur(img, medianBoxSize)
#     # np.ones(サイズ，データ型)：全要素が1の行列を生成。この場合kernelSize*kernelSizeの、全要素が1の行列が用意される。
#     kernel = np.ones((kernelSize, kernelSize), np.uint8)    #np.uint8：NumPyのデータ型のひとつ、符号なし8bit
#     # cv2.morphologyEx(画像，処理，構造要素)：“モルフォロジー”（画像上の図形に対して作用するシンプルな処理）関数
#         # cv2.MORPH_CLOSE：クロージング処理
#     outputImg = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
#     return outputImg

print("START")

img = cv2.imread("./Image.png")
img_GRAY = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow("img_GRAY",img_GRAY)
cv2.waitKey(0)
cv2.imwrite('./GRAY.png', img_GRAY)

BoxSize = 29 # フィルタ用のサイズ指定．奇数のみ．

img_MEDIAN = cv2.medianBlur(img, BoxSize)
cv2.imshow("img_MEDIAN",img_MEDIAN)
cv2.waitKey(0)
cv2.imwrite('./MEDIAN.png', img_MEDIAN)

img_GRAY_MEDIAN = cv2.medianBlur(img_GRAY, BoxSize)
cv2.imshow("img_GRAY_MEDIAN",img_GRAY_MEDIAN)
cv2.waitKey(0)
cv2.imwrite('./GRAY_MEDIAN.png', img_GRAY_MEDIAN)

# ノイズ処理
# noiseReducedImg = reduceNoise(boardImg, 7, 5)
# cv2.imshow("noiseReducedImg",noiseReducedImg)
# cv2.waitKey(0)
# cv2.imwrite('./Results/noiseReducedImg.png', noiseReducedImg)

print("END")