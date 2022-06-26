# img_dgst.py
thumbnail image, histogram and huediagram generator.

実行したカレントディレクトリから再帰的にサブディレクトリの画像を探し、ダイジェスト画像を生成する。<br>
ダイジェスト画像は、色相のグラフ、ヒストグラムと元画像の縮小版を並べたもの。<br>
またExifデータとして元画像のsha256ダイジェストを書きこむ。<br>
ダイジェスト画像の保存先は、カレントディレクトリに掘ったサブディレクトリ"result"以下に、元画像のディレクトリ構成と同じ配置になる。<br>

```
>python img_dgst.py
```

用途は特にない。<br>
<br>
<br>
[課題]<br>
- 保存先のサブディレクトリを予め作っておかないとエラーになる。<br>
- 保存しようとするファイルと同じ名前のファイルが既に存在していると、エラーになる。<br>
- JPEGで保存するためヒストグラムのところに色滲みが出る。<br>
<br>
<br>

[補足]
- 最初は元画像の縮小グレースケール、ヒストグラム、色相環とあと何かをそれぞれ32x32ドットの中に描いて正方形になるように並べる、というものを構想していたが、32x32にまで縮小すると何が描かれているのかよくわからなくなる、32x32の中に色相環を描くと中心付近は解像度が足りずグチャグチャになりそう、などから変更した。<br>
- ヒストグラムは極端に偏ったときでも描画エリアに収まる固定の縮尺で作ろうと思っていたが、ある程度分散すると各BINの値が小さくなり32x32の解像度では潰れて見えなくなってしまう。そのため描画エリア一杯に描くよう画像ごとに縮尺は変えることにした。<br>
- 色相もヒストグラムと同じような棒グラフにして、縮尺も画像ごとに変わるようにした。
- RGBとHSVの変換で値域がよくわからなくて試行錯誤に手間取った。<br>
- モノカラーのサンプル画像をkuritaで作ろうとしたが機能が多すぎてやりにくかった。paint.netに切り替えた。<br>
- pythonとPillowを使ってみたくて、じゃあヒストグラムからいじってみるかということで始めたが、何に使えるかはノーアイデア。<br>
- histogram()はデフォルトでは定義域をa.min()からa.max()にしてしまうらしい。<br>
  最初これに気がつかなくて、なんかおかしいけどどうおかしいのかわからず困ってた。<br>
  モノカラーのサンプル画像で試してようやくずれが分かった。
  histogram()のオプションはいくつかあって関係ないと思ったものはよく読んでなかった。<br>
