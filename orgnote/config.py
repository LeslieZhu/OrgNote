#-*- coding: utf-8 -*-

"""
OrgNote  ---- A simple org-mode blog, write blog by org-mode in Emacs

author: Leslie Zhu
email: pythonisland@gmail.com

Write note by Emacs with org-mode, and convert .org file into .html file,
then use orgnote convert into new html with default theme.
"""

from __future__ import absolute_import

from yaml import load, dump,FullLoader
import os,os.path


class Config(object):

    _default_yml = """# OrgNote Configuration
## Docs: https://orgnote.readthedocs.io/zh_CN/latest/
## Source: https://github.com/LeslieZhu/OrgNote

# Site
title: OrgNote
subtitle: "A simple org-mode blog, write blog by org-mode in Emacs"

author: OrgNote
email: pythonisland@gmail.com

language: zh-CN

# About this blog
description: "Use OrgNote."
keywords: "OrgNote,Emacs,org-mode,blog,python,geek"

# URL
## If your site is put in a subdirectory, set url as 'http://yoursite.com/child' and root as '/child/'
url: http://yoursite.com
root: /


# Directory
# if the source_dir is ./notes, then set 'source_dir' as 'notes', not include the '/'
public_dir: public
source_dir: notes
images_dir: images
files_dir: data


# Category & Tag
default_tag: "默认"

# Nopublic Tab
# public: start with '-'
# nopublic: start with '+'
nopublic_tag: "暂不公开"
reading_mode_keyword: "随笔"

# Theme
# the default is 'freemind' and it's only theme for OrgNote now
theme: freemind

# css highlight
# the defaulit is 'default'
# pygments: manni igor xcode vim autumn vs rrt native perldoc borland tango
# emacs friendly monokai paraiso-dark colorful murphy bw pastie paraiso-light trac default fruity 
css_highlight: default

# Pagination
## the note num of each page
per_page: 6


# duoshuo
duoshuo_shortname:



# layout
## 1: enable
## 0: disable
### if 'sidebar_show` is disable, igore all `sidebar` option
### the sidebar item display as the config order, sidebar items list:
### sidebar_latest,sidebar_tags,sidebar_time,sidebar_weibo,sidebar_link
###
### sidebar_show_page: if show sidebar in each note page,default enable
### sidebar_contain_name: the contain title in sidebar
### sidebar_contact: the contain text in sidebar

sidebar_show: 1
sidebar_show_page: 0

sidebar_contain_name: "联系/反馈"
sidebar_contact: ""

sidebar:
  - sidebar_latest
  - sidebar_tags
  - sidebar_duoshuo
  - sidebar_time
  - sidebar_link


# links, each link should setting url,name,icon
links_title: "友情链接"
links:
  link1:
    url: http://lesliezhu.com
    name: Leslie Zhu
    icon: fa fa-github
  link2:
    url: https://github.com/LeslieZhu/OrgNote
    name: OrgNote
    icon: fa fa-github

# minyi links, add links on menu(MinYi) page
links_minyi_name: "MinYi"
links_minyi:
   link1:
      url: https://github.com/OrgNote
      name: OrgNote

deploy_type: git
deploy_url:
deploy_branch: master
"""

    def __init__(self,cfgfile="_config.yml"):
        self.cfgfile = cfgfile
        self.cfg = dict()
        
        if not os.path.exists(self.cfgfile):
            self.cfg = load(self._default_yml,Loader=FullLoader)
        else:
            self.update()

    def update(self):
        import os.path
        if not os.path.exists(self.cfgfile):
            self.default()

        fp = open(self.cfgfile,"r")
        self.cfg.update(load(fp,Loader=FullLoader))
        fp.close()
        
    def dump(self):
        self.update()
        fp = open(self.cfgfile,"w")
        dump(self.cfg,fp)
        fp.close()

    def default(self):
        fp = open(self.cfgfile,"w")
        fp.write(self._default_yml)
        fp.close()

    def display(self):
        """display the _config.yml contents"""
        for key in  sorted(self.cfg):
            if isinstance(self.cfg[key],dict):
                print(key)
                for key2 in sorted(self.cfg[key]):
                    print("\t",key2,":",self.cfg[key][key2])
            else:
                print(key,":",self.cfg[key])

        
def main(args=None):
    cfg=Config()
    cfg.update()
    cfg.display()
    


if __name__ == "__main__":
    import sys
    sys.exit(main())
