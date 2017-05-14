- 概要

このソフトウェアはMarkdown形式で書いた「メモ」をHTMLとして発行するものです

インストール
-----------------

```
easy_install markdown
easy_install jinja2
pip install py-gfm
pip install mdx_linkify
pip install mdx_del_ins
```

使う
------

```
./webmemo.py -i /Users/kanai/git/PythonJunkScript/WebMemo/articles \
             -o /Users/kanai/WebMemo \
             --year=2014 \
             --month=6 \
             -t /Users/kanai/git/PythonJunkScript/WebMemo/templates
```
