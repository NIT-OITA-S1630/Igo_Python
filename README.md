# メモ
- /Contour_Detect/board_detection.py
    - 碁盤の輪郭を検出して切り取り、あとはPyTest.py(初期ver)と同様の処理を適用。
- /FilterTest
    - 画像処理をいろいろ試してるだけ．たぶんそのうち消す．
- /Input_IMG
    - 入力画像をまとめておく用
- /Results
    - 途中経過を含む、出力画像の保存場所
- PyTest.py
    - メインのやつ．いい加減ファイル名を変えよう．
    - 四隅を指定して盤面を切り取り、点を付与して点周囲の色情報から碁石の有無を判別。

---
- プログラムは殆どが使いまわし。以下参考リンク
    - 碁盤の状態検出の参考にした
        - http://asdm.hatenablog.com/entry/2016/07/26/181700
    - 領域検出（Contour_Detectで実装させてみたやつ。今は後回し。余裕があれば実装したい）
        - https://qiita.com/hatt_takumi/items/47a46d5e85223a41afa4