import cv2
import csv
import numpy as np
import os
if os.name == 'nt': os.system('cls')
else : os.system("clear")

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



im1 = cv2.imread("./A.png")
im2 = cv2.imread("./B.png")

im1_GRAY = cv2.cvtColor(im1,cv2.COLOR_BGR2GRAY)
im2_GRAY = cv2.cvtColor(im2,cv2.COLOR_BGR2GRAY)

im1_GRAY_reduceNoise = reduceNoise(im1_GRAY, 7, 5)
cv2.imwrite('./im1_GRAY_reduceNoise.jpg', im1_GRAY_reduceNoise)   # 差分絶対値を画像化

im2_GRAY_reduceNoise = reduceNoise(im2_GRAY, 7, 5)
cv2.imwrite('./im2_GRAY_reduceNoise.jpg', im2_GRAY_reduceNoise)   # 差分絶対値を画像化

# 通常画像の差分を求める
# im_diff = im1.astype(int) - im2.astype(int) # 差分を求める
# im_diff_abs = np.abs(im_diff)   # 差分を絶対値化
# cv2.imwrite('./im_diff_abs.jpg', im_diff_abs)   # 差分絶対値を画像化

# グレースケール画像の差分を求める
im_GRAY_diff = im1_GRAY_reduceNoise.astype(int) - im2_GRAY_reduceNoise.astype(int) # 差分を求める
im_GRAY_diff_abs = np.abs(im_GRAY_diff)   # 差分を絶対値化
# cv2.imwrite('./im_GRAY_diff_abs.jpg', im_GRAY_diff_abs)   # 差分絶対値を画像化

im_GRAY_diff_BINARY = (im_GRAY_diff_abs > 50) * 255
cv2.imwrite('./im_GRAY_diff_BINARY.jpg', im_GRAY_diff_BINARY)   # 差分絶対値を画像化

print("END")