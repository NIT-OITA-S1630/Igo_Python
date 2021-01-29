# 構成
|  名前  |  内容  |
| ---- | ---- |
|  Figures/  |  生データを使って作成したグラフや，資料作成のためにつくった図など  |
|  Program/  |  ソースコード類  |
|  RawData/  |  実験で使用したデータ，出力されたデータ  |
|  README.md  |  これ  |

# Igo-Python
画像から、碁石の配置を識別するシステム

# Dependence
- Python 3.8.5  
※WSL(Windows Subsystem for Linux)のUbuntuに最初から入っていた。`python3`で実行できる  
（WSLじゃない、Visual StudioのPythonとか、Windowsに直接Pythonを入れるとかの環境で実行確認はしてない）
  
- 必要なパッケージは、./Programs/requirements.txtに記述してある。  
`pip install -r requirements.txt`でまとめてインストールできるはず。  
  
※プログラム内のコメントは、Visual Studio Codeの拡張機能"Better Comments"に合わせた書き方をしています。  
　通常の行コメント(#)に、#!、#?、#TODO 、と書くと色を変えてくれる機能です。  
　プログラムの一部をコメントアウトするとき・行末にコメントするときは通常通り、コメントだけの行は"Better Comments"に合わせた書き方をしていることがあります。

# Setup
- パッケージのインストールについて：省略。上に書いた。
- 実行前に
    - 使用する画像(.jpg)を、RawData/Input_IMG/に入れておくこと
        - ファイル名入力のときに拡張子まで打つのが面倒だった、ってだけでJPGに統一。書き換えればPNGも読み込める。

# Usage
- `python3 pyTest.py`
    - Input filename...：Input_IMGに入れた画像名(拡張子なし)を入力
        - ファイルが無ければ、プログラムは終了する。
        - 指定したファイルが初めて使用するものであれば、以下の処理を行ってプログラムは終了する
            - RawData/Resultsに、画像名のディレクトリを作成
            - 作成されたディレクトリ内に、ptlist.txtを作成
                - このtxtには、盤面の左上、右上、右下、左下、の順で座標を書いておく必要がある。
                - 改行して書くこと（既に作成済みのptlist.txtを参考に）。
    - Input threshold_black (default=52)...
        - 黒石のしきい値の指定。何も打たずにEnterを押すと、def_blackの値（この場合52）が適用される
    - Input threshold_black (default=158)...
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


# Author
- <b><ruby>橋本<rt>はしもと</rt></ruby>　<ruby>燎<rt>りょう</rt></ruby></b> (S1630)

# References
- 色から碁石を識別する方法を実装してた記事
    - 四角形の領域から輝度値を取得する処理とかの参考
    - マスク処理うんぬんは必要性がなかったから消した
    - （中間発表に名残りがある）
    - http://asdm.hatenablog.com/entry/2016/07/26/181700

# Postscript
- Gitはいいぞ
    - フラッシュメモリに入れて持ち歩くのは不便
    - 自宅作業をするつもりならマジで必要
        - 元々するつもりはなかったけど、追い込まれて結局自宅作業をするはめになった。
        - 早いうちに覚悟して、早めに研究室PCと自宅PCにGitを導入するべき。
        - 多分それなりにエラーに遭遇する。non-fast-forwardエラーとか。早めに使い始めて慣れておこう。

- 先行研究はしっかり探しましょう
    - 卒論書き始めてるときに、似たような研究が見つかる、とかいう事態になったらヤバい。
    - 死ぬかと思った。

- Visual Studioはおすすめしない
    - Pythonを使うために最初期にインストールしたが、動作が重い
    - 結局WSL上のPythonを使ってた
    - 普通にWindows上にインストールするのもアリ？
        - 参考にしたWebサイトが大体Linuxでの解説だったから、自分はWSLにした。