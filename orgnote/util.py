#-*- coding: utf-8 -*-

"""
OrgNote  ---- A simple org-mode blog, write blog by org-mode in Emacs

author: Leslie Zhu
email: pythonisland@gmail.com

Write note by Emacs with org-mode, and convert .org file into .html file,
then use orgnote convert into new html with default theme.
"""

from __future__ import absolute_import
from bs4 import BeautifulSoup

import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html as py_html
 
 
class HighlightRenderer(mistune.Renderer):
 
    def block_code(self, code, lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % mistune.escape(code)
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = py_html.HtmlFormatter()
        return highlight(code, lexer, formatter)
 

def gen_title(link=""):
    """ Filter Title from HTML metadata """

    import re
    html_data = BeautifulSoup(open(link,"r").read(),"html.parser")
    obj = html_data.find('h1',{'class':'title'})
    if obj:
        title = obj.text
    else:
        title = link
    return title

def md2html(mdstr=""):
    #import markdown
    
    exts = ['markdown.extensions.extra', 'markdown.extensions.codehilite',
            'markdown.extensions.tables','markdown.extensions.toc',
            'code-friendly', 'fenced-code-blocks', 'footnotes']

    html = '''
    <html lang="zh-cn">
    <head>
    <meta content="text/html; charset=utf-8" http-equiv="content-type" />
    <link href="default.css" rel="stylesheet">
    <link href="github.css" rel="stylesheet">
    </head>
    <body>
    %s
    </body>
    </html>
    '''

    renderer = HighlightRenderer()
    markdown = mistune.Markdown(renderer=renderer)
    ret = markdown(mdstr)
    #ret = markdown.markdown(mdstr,extensions=exts)
    return html % ret

def to_page_mk2(notename=""):
    import codecs,os
    # from orgnote.markdown import Markdown


    css = '''
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<style type="text/css">
</style>
'''


    print("to_page_mk2(%s)" % notename)

    input_file = codecs.open(notename, mode="r", encoding="utf-8")
    text = input_file.read()
    
    # mk = Markdown()
    # html = mk.mk2html(text)

    # print(text)
    # print("="*20)
    # print("="*20)
    
    html = md2html(text)

    html_file = notename.replace(".md",".html")
    output_file = codecs.open(html_file, "w",encoding="utf-8",errors="xmlcharrefreplace")
    output_file.write(html)
    output_file.close()
    print("save to " + html_file)
    

def to_page_mk(notename=""):
    '''
    convert markdown to html
    '''
    import os
    import markdown
    import codecs

    css = '''
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<style type="text/css">
</style>
'''
    
        
    input_file = codecs.open(notename, mode="r", encoding="utf-8")
    text = input_file.read()
    
    if notename.endswith(".md"):
        print(notename)
        print(text)

    html = markdown.markdown(text)
    output_file = codecs.open(notename.replace(".md",".html"), "w",encoding="utf-8",errors="xmlcharrefreplace")
    output_file.write(css+html)

def to_page(notename=""):
    import os,os.path
    try:
        emacs_version = [int(i) for i in get_emacs_version()]
        if emacs_version[0] >= 24:
            #cmd = "emacs -l scripts/ox-html.el --batch %s --funcall org-html-export-to-html 2>/dev/null" % notename
            cmd = "emacs -l scripts/init-orgnote.el --batch %s --funcall org-html-export-to-html 2>/dev/null" % notename
        else:
            cmd = "emacs -l scripts/init-orgnote.el --batch %s --funcall org-export-as-html 2>/dev/null" % notename
            
        print("Run: %s" % cmd)
        os.system(cmd)
    except Exception as ex:
        pass
        #print(">>>>>",str(ex))
        
    html_file = notename.replace('.org','.html')

    #print("html:",html_file)
    #print("\033[32m[Note:]\033[0m: %s generated" % html_file)
    if not os.path.exists(html_file):
        print("\033[31m[ERROR]\033[0m: %s generate FAILED" % html_file)




def add_note(notename="",srcdir="notes/"):
    try:
        import os
        if not notename.endswith('.org'): notename += ".org"
        if not notename.startswith(srcdir): notename = srcdir+"/"+notename
        if not os.path.exists(notename):
            import orgnote.init
            note_name = orgnote.init.create_default_note(notename)
            note_name = note_name.replace("././","./").replace("//","/")
            if note_name != None:
                print("%s init done" % note_name)
                return note_name
        else:
            print("%s exists, please use other name or delete it" % notename)
            return ""
    except Exception as ex:
        return ""
        #print(">>>>>",str(ex))

            
def publish_note(notename="",srcdir="./notes/"):
    try:
        import glob,os.path
        #if notename.endswith(".org"): notename = notename[:-4]
        if notename.startswith(srcdir):
            glob_re = notename
        else:
            glob_re = srcdir+"/????/??/??/%s" % os.path.basename(notename)

        for _file in reversed(sorted(glob.glob(glob_re))):
            if _file.endswith(".org"):
                _html = _file.replace(".org",".html")
                #print(">",_file,_html)
                if not os.path.exists(_html):
                    to_page(_file)                    
            else:
                _html = _file.replace(".md",".html")
                #print(">",_file,_html)
                if not os.path.exists(_html):
                    print("to_page_mk2()",_file)
                    to_page_mk2(_file)

            #_title = gen_title(_html)
            #return "- [[%s][%s]]" % (_html,_title)
            return _file
        return None
    except Exception as ex:
        pass
        #print(">>>>>",str(ex))


def get_emacs_version():
    import os

    return os.popen("emacs --version").readline().strip().split()[-1].split(".")
