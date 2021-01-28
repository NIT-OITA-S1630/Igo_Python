# Igo-Python
画像から，碁石の配置を識別する

# Dependence
Python 3.8.5  
※WSLのUbuntuに最初から入っていた。`python3`で実行できる  
（WSLじゃない、Visual StudioのPythonとか、Windowsに直接Pythonを入れるとかの環境で実行確認はしてない）
  
必要なパッケージは、./Programs/requirements.txtに記述してある。  
`pip install -r requirements.txt`でまとめてインストールできるはず。  
  
※プログラム内のコメントは、Visual Studio Codeの拡張機能"Better Comments"に合わせた書き方をしています。  
　通常の行コメント(#)に、#!、#?、#TODO 、と書くと色を変えてくれる機能です。  
　プログラムの一部をコメントアウトするとき、行末にコメントするときは基本的に通常通り、  
　コメントだけの行は基本的に"Better Comments"に合わせた書き方にしています。

# Setup
- パッケージのインストールについて：省略。上に書いた。
- 実行前に
    - 使用する画像(.jpg)を、RawData/Input_IMG/に入れておくこと
        - ファイル名入力のときに拡張子まで打つのが面倒だった、ってだけでJPGに統一。書き換えればPNGも読み込める。


# Usage
- `python3 pyTest.py`
    - Input filename...：Input_IMGに入れた画像名を入力
        - ファイルが無ければ、プログラムは終了する。
        - 指定したファイルが初めて使用するものであれば、以下の処理を行ってプログラムは終了する
            - RawData/Resultsに、画像名のディレクトリを作成
            - 作成されたディレクトリ内に、ptlist.txtを作成
                - このtxtには、盤面の左上、右上、右下、左下、の順で座標を書いておく必要がある。
                - 改行して書くこと（既に作成済みのptlist.txtを参考に）。
    - Input threshold_black (default=52)
        - 黒石のしきい値の指定。何も打たずにEnterを押すと、def_blackの値（この場合52）が適用される
    - Input threshold_black (default=158)
        - 白石のしきい値の指定。何も打たずにEnterを押すと、def_whiteの値（この場合158）が適用される

- 生成されるファイルについて
    - cornerImg：元画像と、ptlistで指定した四角形を重ねた画像
    - boardImg：ptlistの四角形を、800x800の正方形に変換した画像
    - GRAYImg：boardImgのグレースケール変換
    - noiseReducedImg：GRAYImgのノイズ処理適用後
    - boardWithAreaImg：noiseReducedImg上に、輝度値を取得する領域を緑色の四角形で可視化
    - color_boardWithAreaImg：boardImg上に、同じ緑色の四角形を重ねた
    - result_noiseReduced：noiseReducedImg上に、識別結果のマーカーを重ねた
    - result：グレースケール化したboardImg上に、識別結果のマーカーを重ねた


# Authors
作者を明示する．

# References
参考にした情報源（サイト・論文）などの情報，リンク
[1] [READEMEの良さそうな書き方・テンプレート【GitHub/BitBucket】](https://karaage.hatenadiary.jp/entry/2018/01/19/073000)








# メモ
---
- プログラムは殆どが使いまわし。以下参考リンク
    - 碁盤の状態検出の参考にした
        - http://asdm.hatenablog.com/entry/2016/07/26/181700
    - 領域検出（Contour_Detectで実装させてみたやつ。今は後回し。余裕があれば実装したい）
        - https://qiita.com/hatt_takumi/items/47a46d5e85223a41afa4