#-*- coding: utf-8 -*-

"""
OrgNote  ---- A simple org-mode blog, write blog by org-mode in Emacs

author: Leslie Zhu
email: pythonisland@gmail.com

Write note by Emacs with org-mode, and convert .org file into .html file,
then use orgnote convert into new html with default theme.
"""

from __future__ import absolute_import

from yaml import load, dump


class Config(object):

    _default_yml = """# OrgNote Configuration
## Docs: http://lesliezhu.github.io/OrgNote/
## Source: https://github.com/LeslieZhu/OrgNote

# Site
title: OrgNote
subtitle: "A simple org-mode blog, write blog by org-mode in Emacs"
description: "A simple org-mode blog, write blog by org-mode in Emacs"
author: Leslie Zhu
email:
language: zh-CN

# URL
## If your site is put in a subdirectory, set url as 'http://yoursite.com/child' and root as '/child/'
url: http://yoursite.com
root: /
permalink: :year/:month/:day/:title/
tag_dir: tags
archive_dir: archives

# Directory
source_dir: notes
public_dir: public

# Category & Tag
default_tag: 札记
tag_map:

# Archives
## 2: Enable pagination
## 1: Disable pagination
## 0: Fully Disable
archive: 2
category: 2
tag: 2

# Server
port: 4000
server_ip: 0.0.0.0

# Pagination
## Set per_page to 0 to disable pagination
per_page: 10
pagination_dir: page

# duoshuo
duoshuo_shortname:

# Extensions
theme: freemind
exclude_generator:

# Deployment
deploy:
  type: git
"""

    def __init__(self,cfgfile="_config.yml"):
        self.cfgfile = cfgfile
        self.cfg = load(self._default_yml)

    def update(self):
        import os.path
        if not os.path.exists(self.cfgfile):
            self.default()

        fp = open(self.cfgfile,"r")
        self.cfg = load(fp)
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
        for key in  self.cfg:
            print key,":",self.cfg[key]

        
def main(args=None):
    cfg=Config()
    cfg.update()
    cfg.display()
    


if __name__ == "__main__":
    import sys
    sys.exit(main())
