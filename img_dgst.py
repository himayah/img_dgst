import glob
import re
import os
import numpy as np
from PIL import Image, ImageDraw
import colorsys
import pyexiv2
import hashlib


path = 'result'
os.makedirs(path, exist_ok=True)

files = [file for file in glob.glob("./**/*", recursive=True) if not re.search('(\.txt$|\.bat$|\.py$)', file) if os.path.isfile(file)]

for file in files:
    # 横64 x 縦96、白背景のキャンバスを用意
    img_base = Image.new('RGB', (64, 96), (255, 255, 255))
    draw = ImageDraw.Draw(img_base)

    # Pillowで読み込み
    with Image.open(file) as img:
        # 画像をHSV化
        h, s, v = img.convert('HSV').split()

        # Ｓ（彩度）が0のドットは捨て、残ったドットについてのみヒストグラムを取る。
        h_hsv = [h.getdata()[i] for i in range(len(s.getdata())) if s.getdata()[i] != 0]

        # 画像をモノクロ化
        img_mono = img.convert('L')

        # 元画像を64x64サイズに縮小して表示（64x96のキャンバスの(0,32)-(63,95)）
        x_ratio = 64 / img.width
        y_ratio = 64 / img.height

        # 64x64の白いキャンバスに縮小したモノクロ画像をセンタリング貼り付け
        if x_ratio > y_ratio:
            simg = img.resize((round(img.width * y_ratio), 64))
            img_base.paste(simg, (round((64 - simg.width) / 2), 32))
        else:
            simg = img.resize((64, round(img.height * x_ratio)))
            img_base.paste(simg, (0, round((64 - simg.height) / 2) + 32))

    # Numpyでヒストグラム化。31階調、最大値が27になるように縮小。
    hist_hsv, bins = np.histogram(h_hsv, 31, (0, 255))
    chist_hsv = [ht * 27 / np.amax(hist_hsv) for ht in hist_hsv]

    # Numpyでヒストグラム化。31階調、最大値が27になるように縮小。
    hist_mono, bins = np.histogram(img_mono, 31, (0, 255))
    chist_mono = [ht * 27 / np.amax(hist_mono) for ht in hist_mono]

    # 階調の各段ごとに手続き
    for x in range(31):
        # Ｈ（彩度）の描画（64x96のキャンバスの(0,0)-(31,31)）
        r, g, b = colorsys.hsv_to_rgb(x / 31, 1, 1)

        # 下から4ドット目からこの階調の値分の長さの線を描く
        draw.line((x, 27, x, 27 - round(chist_hsv[x])), fill=(round(r * 256), round(g * 256), round(b * 256)))

        # 色見本を2ドット幅で描く
        draw.line((x, 30, x, 29), fill=(round(r * 256), round(g * 256), round(b * 256)))

        # ヒストグラムの描画（64x96のキャンバスの(32,0)-(63,31)）
        # この階調の値分の長さの線を描く
        draw.line((x + 32, 27, x + 32, 27 - round(chist_mono[x])), fill=(0, 0, 0))

        # 階調のサンプルを2ドット幅で描く
        draw.line((x + 32, 30, x + 32, 29), fill=(round(x * 8), round(x * 8), round(x * 8)))

    img_base.save(os.path.join(path, file[2:]), quality=75)

    # ファイルオープン
    with pyexiv2.Image(os.path.join(path, file[2:])) as img:
        # メタデータ read
        metadata = img.read_exif()

        with open(file, 'rb') as fp:
            fileData = fp.read()
        hs256 = hashlib.sha256(fileData).hexdigest()

        # コメント を ハッシュ値 に書き換え
        metadata["Exif.Image.XPComment"] = "Original Image's sha256 : " + hs256

        # メタデータ を img に書き戻し
        img.modify_exif( metadata )


# あらかじめ保存先のサブフォルダがないとエラー、
# 保存先に同じ名前のファイルが既に存在していてもエラー？
