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


def gen_title(link=""):
    """ Filter Title from HTML metadata """

    import re
    html_data = BeautifulSoup(open(link,"r").read(),"html.parser")
    title = html_data.find('h1',{'class':'title'}).text
    return title

def to_page_mk2(notename=""):
    from orgnote.markdown import Markdown

    print("to_page_mk2(%s)" % notename)

    input_file = codecs.open(notename, mode="r", encoding="utf-8")
    text = input_file.read()
    
    mk = Markdown()
    
    print("*" * 20)
    print(text)
    print("*" * 20)
    
    html = mk.mk2html(text)
    
    output_file = codecs.open(notename.replace(".md",".html"), "w",encoding="utf-8",errors="xmlcharrefreplace")
    output_file.write(css+html)

    

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
            cmd = "emacs -l scripts/ox-html.el --batch %s --funcall org-html-export-to-html 2>/dev/null" % notename
            #cmd = "emacs -l scripts/init-orgnote.el --batch %s --funcall org-html-export-to-html 2>/dev/null" % notename
        else:
            cmd = "emacs -l scripts/init-orgnote.el --batch %s --funcall org-export-as-html 2>/dev/null" % notename
        os.system(cmd)
        html_file = notename.replace('.org','.html')
        print("html:",html_file)
        if os.path.exists(html_file):
            print("==> %s generated" % html_file)
        else:
            print("==> %s generat FAILED" % html_file)
    except Exception as ex:
        print(">>>>>",str(ex))


def add_note(notename=""):
    try:
        import os
        if not notename.endswith('.org'): notename += ".org"
        if not notename.startswith('notes/'): notename = "notes/"+notename
        if not os.path.exists(notename):
            import orgnote.init
            note_name = orgnote.init.create_default_note(notename)
            if note_name != None:
                print("%s init done" % note_name)
        else:
            print("%s exists, please use other name or delete it" % notename)
    except Exception as ex:
        print(">>>>>",str(ex))

            
def publish_note(notename=""):
    try:
        import glob,os.path
        #if notename.endswith(".org"): notename = notename[:-4]
        if notename.startswith("./notes"):
            glob_re = notename
        else:
            glob_re = "./notes/????/??/??/%s" % os.path.basename(notename)

        for _file in reversed(sorted(glob.glob(glob_re))):
            if _file.endswith(".org"):
                _html = _file.replace(".org",".html")
                #print(">",_file,_html)
                if not os.path.exists(_html):
                    to_page(_file)                    
            else:
                _html = _file.replace(".md",".html")
                print(">",_file,_html)
                if not os.path.exists(_html):
                    print("to_page_mk2()",_file)
                    to_page_mk2(_file)

            _title = gen_title(_html)
            return "- [[%s][%s]]" % (_html,_title)
        return None
    except Exception as ex:
        print(">>>>>",str(ex))


def get_emacs_version():
    import os

    return os.popen("emacs --version").readline().strip().split()[-1].split(".")
