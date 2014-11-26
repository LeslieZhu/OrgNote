#-*- coding: utf-8 -*-

from __future__ import absolute_import

def create_emacs_init():
    """
    init ./scripts/init-orgnote.el
    """

    import os
    import os.path

    _dirname = "./scripts/"
    _init_file = _dirname + "init-orgnote.el"

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
        print "[info] create ",_init_file
        output = open(_init_file,"w")
        print >> output,_data
        output.close()

def create_default_note(name="HelloOrgNote.org"):
    """
    init notes/template.org
    """

    import os
    import os.path

    _dirname = "./notes/"
    _init_file = _dirname + name

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
#+LANGUAGE: zh-CN
        
#+KEYWORDS: 标签
#+TITLE: 标题
#+AUTHOR: 作者
#+EMAIL: 作者邮件
#+DATE: 10/1/2014

* HelloOrgNote

[[https://github.com/LeslieZhu/OrgNote][OrgNote]] is a simple blog based on org-mode, enjoy it:)
"""


    if not os.path.exists(_dirname):
        os.mkdir(_dirname)

    if not os.path.exists(_init_file):
        print "[info] create ",_init_file
        output = open(_init_file,"w")
        print >> output,_data
        output.close()
    elif name != "HelloOrgNote.org":
        print "File %s already exists, please use a new name!" % name

def create_config_file(name="_config.py"):
    """
    init _config.py config file
    """

    import os
    import os.path

    _name = os.path.expanduser(name)
    if not os.path.exists(_name):
        print "[info] create ",_name
        import orgnote.config
        orgnote.config.main()
    #else:
    #    print "[info] config info.."
    #    with open(_name) as cin:
    #        print cin.next()


def create_public_file(name = "public.org"):
    """
    init ./notes/public.org
    """
    
    import os
    import os.path

    _dir = "./notes/"
    _init_file = _dir + name

    if name == "public.org":
        _data = """# for example:
# - [[./HelloOrgNote.html][HelloOrgNote]]
- [[./HelloOrgNote.html][HelloOrgNote]]
        """
    else:
        _data = """# for example:
# + [[./HelloOrgNote.html][HelloOrgNote]]
        """

    if not os.path.exists(_dir):
        os.mkdir(_dir)

    if not os.path.exists(_init_file):
        print "[info] create ",_init_file
        output = open(_init_file,"w")
        print >> output,_data
        output.close()
    

def main(args=None):
    import os
    import os.path
    
    target_list = ["./theme/","./notes/","./scripts/","./public/","./public/tags/"]

    for target in target_list:
        if not os.path.exists(target):
            print "[info] create ",target
            os.mkdir(target)

    # init files
    create_emacs_init()
    create_default_note()
    #create_config_file()
    create_config_file("_config.py")
    create_public_file("public.org")
    create_public_file("nopublic.org")


if __name__ == "__main__":
    import sys
    sys.exit(main())
