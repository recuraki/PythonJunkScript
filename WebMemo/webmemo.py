#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Web Wiki作成するよ
"""

import sys
import time
import optparse
import markdown
import jinja2
import os
import glob
import re
import codecs

reload(sys)
sys.setdefaultencoding('utf-8')

def option_parse():
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
    with codecs.open(fnInput, mode="r", encoding="utf-8") as fd:
        codehilite = 'codehilite(force_linenos=True, guess_lang=False, css_class=syntax)'
        html = markdown.markdown(fd.read(), ['extra', codehilite, 'gfm' ])
    fd.close()
    return(html.encode('utf-8'))

def proc_specific_dir(arg, liExistMonth = []):
    
    d_input = arg.o_inputdir + "/" + "%04d/%02d" % (arg.o_targetyear, arg.o_targetmonth)
    liMd = glob.glob(d_input + "/*.md")

    if liMd != None:
        liMd.reverse()
        
    article = []
    
    for fnMd in liMd:
        diDate = {}
        stDate = ""
        fnBase = os.path.basename(fnMd)
        m = re.match(r"^(\d{4})(\d{2})(\d{2})", fnBase)
        if m:
            diDate['year'] = m.group(1)
            diDate['month'] = m.group(2)
            diDate['day'] = m.group(3)
            stDate = "{0}年{1}月{2}日".format(diDate['year'], diDate['month'], diDate['day'])
        html = md2html(fnMd)
        article.append({"html": html, "stDate": stDate})
    env   = jinja2.Environment(loader=jinja2.FileSystemLoader(arg.o_template, encoding='utf-8'))
    templ = env.get_template("index.html")
    html  = templ.render(article = article)
    return(html)
    

def proc_output(arg, html):
    stOutpath = arg.o_outputdir + "/" +  "%04d%02d.html" % (arg.o_targetyear, arg.o_targetmonth)
    with codecs.open(stOutpath, mode = "w", encoding = "utf-8") as fd:
        fd.write(html)
        fd.close()
    
if __name__ == "__main__":
    arg = option_parse()
    if arg.f_targetall:
        for stDir in glob.glob(arg.o_inputdir + "/*/*"):
            stYear, stMonth =  tuple(stDir.split("/")[-2:])
            arg.o_targetyear, arg.o_targetmonth = int(stYear), int(stMonth)
            html = proc_specific_dir(arg)
            proc_output(arg, html)

    if arg.o_targetyear != 0 and arg.o_targetmonth != 0:
        html = proc_specific_dir(arg)
        proc_output(arg, html)
