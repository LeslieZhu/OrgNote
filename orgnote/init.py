#-*- coding: utf-8 -*-

"""
OrgNote  ---- A simple org-mode blog, write blog by org-mode in Emacs

author: Leslie Zhu
email: pythonisland@gmail.com

Write note by Emacs with org-mode, and convert .org file into .html file,
then use orgnote convert into new html with default theme.
"""
from __future__ import print_function
from __future__ import absolute_import

import os,os.path


def create_emacs_init(initfile="init-orgnote.el"):
    """
    init ./scripts/init-orgnote.el
    """

    import os
    import os.path

    _dirname = "./scripts/"
    _init_file = _dirname + initfile

    _data = """;; 设置org-mode输出中文目录
(custom-set-variables
 '(org-blank-before-new-entry
      (quote ((heading) (plain-list-item))))

 '(org-export-language-setup
      (quote
               (("en" "Author" "Date" "Table of Contents" "Footnotes") ("zh-CN" "作者" "日期" "目录" "脚注")))))
 """

    if not os.path.exists(_dirname):
        os.mkdir(_dirname)

    if not os.path.exists(_init_file):
        print("[info] create ",_init_file)
        output = open(_init_file,"w")
        print(_data,file=output)
        output.close()

def create_about_html(name="about.hmtl"):
    import os
    import os.path
    import time
    
    import orgnote.parser
    blog = orgnote.parser.OrgNote()

    _data =  """
    <html>
    <head>
    <meta name="keywords" content="关于" />
    </head>
    <body>
    <div id="content">
    <h1 class="title"></h1>
    <p>
    此博客 <code>OrgNote</code> 基于<a href="https://github.com/LeslieZhu/OrgNote">OrgNote</a>生成。
    </p>
    </div>
    </body>
    </html>
    """

    
    _dirname = blog.source_dir
    _init_file = _dirname + os.path.basename(name)

    if not os.path.exists(_dirname):
        os.makedirs(_dirname)

    if not os.path.exists(_init_file):
        print("[info] create ",_init_file)
        output = open(_init_file,"w")
        print(_data,file=output)
        output.close()
        return _init_file
    else:
        print("File %s already exists, please use a new name!" % _init_file)
        return None

def create_note_file(name="links.org",text=[]):
    import os
    import orgnote.parser
    
    blog = orgnote.parser.OrgNote()
    
    _dirname = blog.source_dir
    _init_file = _dirname + os.path.basename(name)

    if not os.path.exists(_dirname):
        os.makedirs(_dirname)

    if not os.path.exists(_init_file):
        print("[info] create ",_init_file)
        output = open(_init_file,"w")
        for i in text:
            print(i,file=output)
        output.close()
        return _init_file
    else:
        print("File %s already exists, please use a new name!" % _init_file)
        return None

    
def create_about_note(name="about.org"):
    import os
    import os.path
    import time

    import orgnote.parser
    blog = orgnote.parser.OrgNote()

    _data =  """#+STARTUP: overview
#+STARTUP: content
#+STARTUP: showall
#+STARTUP: showeverything
#+STARTUP: indent
#+STARTUP: nohideblocks
#+OPTIONS: ^:{}
#+OPTIONS: LaTeX:t
#+OPTIONS: LaTeX:dvipng
#+OPTIONS: LaTeX:nil
#+OPTIONS: LaTeX:verbatim
        
#+OPTIONS: H:3
#+OPTIONS: toc:t
#+OPTIONS: num:t
#+LANGUAGE: %s
        
#+KEYWORDS: 关于
#+TITLE: 关于此博客
#+AUTHOR: %s
#+EMAIL: %s
#+DATE: %s

此博客 =%s= 基于[[https://github.com/LeslieZhu/OrgNote][OrgNote]]生成。
""" % (blog.language, blog.author,blog.email,time.strftime("%Y/%m/%d",time.localtime()),blog.title)

    
    _dirname = blog.source_dir
    _init_file = _dirname + os.path.basename(name)

    if not os.path.exists(_dirname):
        os.makedirs(_dirname)

    if not os.path.exists(_init_file):
        print("[info] create ",_init_file)
        output = open(_init_file,"w")
        print(_data,file=output)
        output.close()
        return _init_file
    else:
        print("File %s already exists, please use a new name!" % _init_file)
        return None


def create_md_note(name="HelloOrgNote.md"):
    import os
    import os.path
    import time

    import orgnote.parser
    
    blog = orgnote.parser.OrgNote()
    
    _dirname = blog.source_dir + time.strftime("%Y/%m/%d",time.localtime())
    _init_file = _dirname + "/" + os.path.basename(name)

    _data = """---
title: %s
date: %s
tags: %s
---

# %s
"""
    _data = _data % (name,time.strftime("%Y/%m/%d",time.localtime()),blog.default_tag,name)

    if not os.path.exists(_dirname):
        os.makedirs(_dirname)

    if not os.path.exists(_init_file):
        print("[info] create ",_init_file)
        output = open(_init_file,"w")
        print(_data,file=output)
        output.close()
        return _init_file
    else:
        print("File %s already exists, please use a new name!" % _init_file)
        return None
    
def create_default_note(name="HelloOrgNote.org"):
    """
    init source_dir/template.org
    """

    import os
    import os.path
    import time

    import orgnote.parser
    blog = orgnote.parser.OrgNote()

    _data =  """#+STARTUP: overview
#+STARTUP: content
#+STARTUP: showall
#+STARTUP: showeverything
#+STARTUP: indent
#+STARTUP: nohideblocks
#+OPTIONS: ^:{}
#+OPTIONS: LaTeX:t
#+OPTIONS: LaTeX:dvipng
#+OPTIONS: LaTeX:nil
#+OPTIONS: LaTeX:verbatim
        
#+OPTIONS: H:3
#+OPTIONS: toc:t
#+OPTIONS: num:t
#+LANGUAGE: %s
        
#+KEYWORDS: %s
#+TITLE: %s
#+AUTHOR: %s
#+EMAIL: %s
#+DATE: %s

* Hello OrgNote

[[https://github.com/LeslieZhu/OrgNote][OrgNote]] is a simple blog based on org-mode, enjoy it:)
""" % (blog.language, blog.default_tag, os.path.basename(name).strip(".org"),
       blog.author,blog.email,time.strftime("%Y/%m/%d",time.localtime()))

    
    _dirname = blog.source_dir + time.strftime("%Y/%m/%d",time.localtime())
    _init_file = _dirname + "/" + os.path.basename(name)

    if not os.path.exists(_dirname):
        os.makedirs(_dirname)

    if not os.path.exists(_init_file):
        print("[info] create ",_init_file)
        output = open(_init_file,"w")
        print(_data,file=output)
        output.close()
        return _init_file
    else:
        print("File %s already exists, please use a new name!" % _init_file)
        return None


def create_config_file(name="_config.yml"):
    """
    init _config.yml config file
    """

    import os
    import os.path
    
    _dir = "./"
    _init_file = _dir + name

    if not os.path.exists(_init_file):
        print("[info] create ",_init_file)
        import orgnote.config
        orgnote.config.Config().default()


def create_public_file(name = "public.org"):
    """
    init ./source_dir/public.org
    """
    
    import os
    import os.path
    import orgnote.parser
    blog = orgnote.parser.OrgNote()

    _dir = blog.source_dir
    _init_file = _dir + name

    if name == "public.org":
        _data = """"""
    else:
        _data = """"""

    if not os.path.exists(_dir):
        os.mkdir(_dir)

    if not os.path.exists(_init_file):
        print("[info] create ",_init_file)
        output = open(_init_file,"w")
        print(_data,file=output)
        output.close()
    

def main(args=None):
    import os
    import os.path
    import orgnote.parser
    blog = orgnote.parser.OrgNote()

    create_config_file("_config.yml")

    source_dir = blog.source_dir
    public_dir = blog.public_dir
    tags_dir = public_dir + "/tags/"
    
    target_list = ["./theme/",public_dir,tags_dir,source_dir]

    for target in target_list:
        if not os.path.exists(target):
            print("[info] create ",target)
            os.mkdir(target)

    # init files
    #create_emacs_init("init-orgnote.el")
    create_public_file("public.org")
    create_public_file("nopublic.org")
    create_about_note(blog.source_dir + "/about.org")
    create_about_html(blog.source_dir + "/about.html")

    link = ["https://github.com/LeslieZhu/OrgNote, OrgNote:为自己定制的基于org-mode博客工具, fa fa-github"]
    create_note_file(blog.source_dir + "/links.org",link)
    create_note_file(blog.source_dir + "/slinks.org",link)

    job_once = "by_once,2019/11/11 10:00,查看OrgNote更新,https://github.com/LeslieZhu/OrgNote"
    job_day = "by_day,2019/11/11 10:00,查看OrgNote更新,https://github.com/LeslieZhu/OrgNote"
    job_week = "by_week,2019/11/11 10:00,查看OrgNote更新,https://github.com/LeslieZhu/OrgNote"
    job_month = "by_month,2019/11/11 10:00,查看OrgNote更新,https://github.com/LeslieZhu/OrgNote"
    job_quarter = "by_quarter,2019/11/11 10:00,查看OrgNote更新,https://github.com/LeslieZhu/OrgNote"
    job_year = "by_year,2019/11/11 10:00,查看OrgNote更新,https://github.com/LeslieZhu/OrgNote"
    create_note_file(blog.source_dir + "/calendar.org",[job_once,job_day,job_week,job_month,job_quarter,job_year])
    #create_default_note(blog.source_dir + "/HelloOrgNote.org")


    if not os.path.exists("theme/freemind"):
        cmd = "git clone git@github.com:LeslieZhu/orgnote-theme-freemind.git theme/freemind"
        os.system(cmd)
        cmd = "rm -rf theme/freemind/.git"
        os.system(cmd)
    if not os.path.exists("scripts"):
        cmd = "git clone git@github.com:LeslieZhu/orgnote-emacs-el.git scripts/"
        os.system(cmd)
        cmd = "rm -rf scripts/.git"
        os.system(cmd)


if __name__ == "__main__":
    import sys
    sys.exit(main())
