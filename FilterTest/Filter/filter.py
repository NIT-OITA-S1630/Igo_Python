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


# ノイズ処理
noiseReducedImg = reduceNoise(boardImg, 7, 5)
cv2.imshow("noiseReducedImg",noiseReducedImg)
cv2.waitKey(0)
cv2.imwrite('./Results/noiseReducedImg.png', noiseReducedImg)