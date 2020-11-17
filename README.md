# メモ
- PyTest.py
    - 四隅を指定して盤面を切り取り、点を付与して点周囲の色情報から碁石の有無を判別。
- /Input_IMG
    - 入力画像をまとめておく用
- /Results
    - 途中経過を含む、出力画像の保存場所

- Contour_Detect/board_detection.py
    - 碁盤の輪郭を検出して切り取り、あとはPyTest.pyと同様の処理を適用。
---
- プログラムは殆どが使いまわし。以下参考リンク
    - 碁盤の状態検出の参考にした
        - http://asdm.hatenablog.com/entry/2016/07/26/181700
    - 領域検出（Contour_Detectで実装させてみたやつ。今は後回し。余裕があれば実装したい）
        - https://qiita.com/hatt_takumi/items/47a46d5e85223a41afa4

- HTTPSからSSH接続に切り替え。変更確認用の試し書き！
- 試しに変更