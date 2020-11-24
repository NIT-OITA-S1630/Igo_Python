import cv2
import numpy as np
import matplotlib.pyplot as plt

import os
if os.name == 'nt': os.system('cls')
else : os.system("clear")

print("START")

def plot_grayscale_conversion(src, dst):
    fig = plt.figure(figsize=(10, 6))
    ax1 = plt.subplot2grid((3, 2), (0, 0), rowspan=2)
    ax2 = plt.subplot2grid((3, 2), (0, 1), rowspan=2)
    ax3 = plt.subplot2grid((3, 2), (2, 0))
    ax4 = plt.subplot2grid((3, 2), (2, 1))
    # 入力画像を描画する。
    ax1.set_title("Input")
    ax1.imshow(src, cmap="gray", vmin=0, vmax=255)
    ax1.set_axis_off()
    # 出力画像を描画する。
    ax2.set_title("Output")
    ax2.imshow(dst, cmap="gray", vmin=0, vmax=255)
    ax2.set_axis_off()
    # 入力画像のヒストグラムを描画する。
    ax3.hist(src.ravel(), bins=256, range=(0, 255), color="k")
    ax3.grid()
    ax3.set_xticks([0, 255])
    ax3.set_yticks([])
    # 出力画像のヒストグラムを描画する。
    ax4.hist(dst.ravel(), bins=256, range=(0, 255), color="k")
    ax4.set_xticks([0, 255])
    ax4.set_yticks([])
    ax4.grid()



# 処理開始



img = cv2.imread("Image.png", cv2.IMREAD_GRAYSCALE)

# ポスタリゼーション
x = np.arange(256)
n = 3  # 画素値を何段階で表現するか
bins = np.linspace(0, 255, n + 1)
y = np.array([bins[i - 1] for i in np.digitize(x, bins)]).astype(int)

img_MEDIAN = cv2.medianBlur(img, 11)

# 変換する。
dst = cv2.LUT(img_MEDIAN, y)

#画像の表示
plt.gray() # 表示カラーマップをグレースケールとする(*)
plt.imshow(dst)
plt.show()


# plot_grayscale_conversion(img, dst)

print("END")