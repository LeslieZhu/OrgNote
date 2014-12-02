#-*- coding: utf-8 -*-

"""
OrgNote  ---- A simple org-mode blog, write blog by org-mode in Emacs

author: Leslie Zhu
email: pythonisland@gmail.com

Write note by Emacs with org-mode, and convert .org file into .html file,
then use orgnote convert into new html with default theme.
"""

from __future__ import absolute_import


def gen_title(link=""):
    """ Filter Title from HTML metadata """

    import re
    title = ""
    for line in open(link).readlines():
        if "<title>" in line:
            line = line.strip()
            title=re.match("<title>(.*)</title>",line).groups(1)[0]
            break
    return title


def to_page(notename=""):
    import os
    try:
        os.system("emacs -l scripts/init-orgnote.el --batch %s --funcall org-export-as-html 2>/dev/null" % notename)
        print "%s generated" % notename.replace('.org','.html')
    except Exception,ex:
        print str(ex)


def add_note(notename=""):
    try:
        import os
        if not notename.endswith('.org'): notename += ".org"
        if not notename.startswith('notes/'): notename = "notes/"+notename
        if not os.path.exists(notename):
            import orgnote.init
            note_name = orgnote.init.create_default_note(notename)
            if note_name != None:
                print "%s init done" % note_name
        else:
            print "%s exists, please use other name or delete it" % notename
    except Exception,ex:
        print str(ex)

            
def publish_note(notename=""):
    try:
        import glob,os.path
        if notename.endswith(".org"): notename = notename[:-4]
        for _file in glob.glob("./notes/????/??/??/%s.org" % notename):
            _html = _file.replace(".org",".html")
            if not os.path.exists(_html):
                to_page(_file)
            _title = gen_title(_html)
            return "- [[%s][%s]]" % (_html,_title)
        return None
    except Exception,ex:
        print str(ex)
