#!/usr/bin/python
# coding: utf-8

"""
base.pngを読み込み、
第二引数に指定された文字列を左上に印字し、
第一引数に指定されたファイルに書き込みます。
"""

import Image
import ImageDraw
import ImageFont
import sys,os

def main(file, text):
    _bg = Image.open("base.png")
    _draw = ImageDraw.Draw(_bg)
    _font = ImageFont.truetype("/Library/Fonts/Arial Unicode.ttf",22, encoding="utf-8")
    _draw.text((0,0), text, font=_font)
    _bg.save(file)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
