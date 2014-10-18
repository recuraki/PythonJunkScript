#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Web Wiki作成するよ
easy_install markdown
easy_install jinja2
mkdir ~/tmp
cd ~/tmp
git clone https://github.com/dart-lang/py-gfm.git
cd py-gfm
python setup.py install
sudo pip install mdx_linkify
sudo  pip install mdx_del_ins
"""

# 標準ライブラリのインポート
import sys
import time
import optparse
import os
import glob
import re
import codecs

# pipからのインストールが必要
import markdown
import jinja2

# 文字コード対策
reload(sys)
sys.setdefaultencoding('utf-8')

def option_parse():
    """
    オプションパース用の関数
    """
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="o_inputdir", action="store", default="")
    parser.add_option("-o", "--output",dest="o_outputdir", action="store"   ,default="")
    parser.add_option("-y", "--year",  dest="o_targetyear", action="store"  ,default=0, type="int")
    parser.add_option("-m", "--month", dest="o_targetmonth", action="store" ,default=0, type="int")
    parser.add_option("-a", "--all",   dest="f_targetall", action="store_true" ,default=False)
    parser.add_option("-t", "--template",   dest="o_template", action="store" ,default="")
    (options, args) = parser.parse_args()
    return(options)

def md2html(fnInput):
    """
    MarkDownファイルからHTMLを作成する
    @fnInput: 入力MarkDownファイル
    """
    
    with codecs.open(fnInput, mode="r", encoding="utf-8") as fd:
        # MarkDownを作成する際に、コードハイライトを有効にする(ためのオプションの変数)
        codehilite = 'codehilite(force_linenos=True, guess_lang=False, css_class=syntax)'
        # MarkDownファイルからHTMLを作成
        html = markdown.markdown(fd.read(), ['extra', codehilite, 'gfm' ])
    fd.close()
    # htmlをUTF-8にエンコードして返す
    return(html.encode('utf-8'))

def proc_specific_dir(arg, liExistMonth = []):
    """
    指定された年月のmdファイルからhtmlを作成する
    """

    
    # 入力ディレクトリはdir/2014/09のように示される
    d_input = arg.o_inputdir + "/" + "%04d/%02d" % (arg.o_targetyear, arg.o_targetmonth)

    # 入力ディレクトリに存在する.mdのファイルすべてのリストを作成する(処理対象リスト)
    liMd = glob.glob(d_input + "/*.md")

    # 最新のメモを先に持ってきたいので、Reverse(昇順の逆＝降順）とする
    if liMd != None:
        liMd.sort()
        liMd.reverse()


    # 各ファイルの処理を実施
    article = []
    for fnMd in liMd:
        """
        処理対象リストの各MarkDownファイルを処理する
        """
        diDate = {}
        stDate = ""
        fnBase = os.path.basename(fnMd)
        # それぞれのファイルは20140901.mdのようなYYYYMMDDで示されることを前提とする
        # 尚、日時がパース出来なかった場合、日付は出力されない
        m = re.match(r"^(\d{4})(\d{2})(\d{2})", fnBase)
        if m:
            """
            ここではstDateに日付を格納する
            """
            diDate['year'] = m.group(1)
            diDate['month'] = m.group(2)
            diDate['day'] = m.group(3)
            stDate = "{0}年{1}月{2}日".format(diDate['year'], diDate['month'], diDate['day'])
        # 処理対象のファイルをhtmlに変換する
        html = md2html(fnMd)
        # 変換したhtmlをarticleに追記していく
        article.append({"html": html, "stDate": stDate})
    """
    ここで、articleは「テンプレート」に含まれる特殊な変数とする。
    jinja2にてテンプレートから最終的に出力する文字列を生成する
    """
    env   = jinja2.Environment(loader=jinja2.FileSystemLoader(arg.o_template, encoding='utf-8'))
    templ = env.get_template("index.html")

    """
    ここでheaderは「テンプレート」のなかの特殊な変数
    実際は固定的なコンテンツからファイルを読み込みます
    """
    fnHeader = arg.o_inputdir + "/" + "header.md"
    header_content = ""
    # ファイルが存在するときのみの処理
    if os.path.exists(fnHeader):
        # 通常の記事ファイルと同様の処理を行います
        with codecs.open(fnHeader, mode = "r", encoding = "utf-8") as fd:
            header_content = md2html(fnHeader)
            fd.close()
    
    html  = templ.render(article = article, header_content = header_content)
    # jinja2によって生成された文字列を返す
    return(html)
    

def proc_output(arg, html):
    """
    結果をファイルに出力します
    """
    stOutpath = arg.o_outputdir + "/" +  "%04d%02d.html" % (arg.o_targetyear, arg.o_targetmonth)
    with codecs.open(stOutpath, mode = "w", encoding = "utf-8") as fd:
        fd.write(html)
        fd.close()
    
if __name__ == "__main__":
    arg = option_parse()
    if arg.f_targetall:
        print("making all articles...")
        for stDir in glob.glob(arg.o_inputdir + "/*/*"):
            stYear, stMonth =  tuple(stDir.split("/")[-2:])
            arg.o_targetyear, arg.o_targetmonth = int(stYear), int(stMonth)
            print("  [proc]" + stYear + "/" + stMonth)
            html = proc_specific_dir(arg)
            proc_output(arg, html)

    if arg.o_targetyear != 0 and arg.o_targetmonth != 0:
        html = proc_specific_dir(arg)
        proc_output(arg, html)
