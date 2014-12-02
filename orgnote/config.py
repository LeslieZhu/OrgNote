#-*- coding: utf-8 -*-

"""
OrgNote  ---- A simple org-mode blog, write blog by org-mode in Emacs

author: Leslie Zhu
email: pythonisland@gmail.com

Write note by Emacs with org-mode, and convert .org file into .html file,
then use orgnote convert into new html with default theme.
"""

from __future__ import absolute_import

import ConfigParser

class Config(object):
    def __init__(self,cfgfile="_config.ini"):
        self.cfgfile = cfgfile
        self.fp = ConfigParser.ConfigParser()
        self.fp.optionxform = str
        self.cfg = dict()

        self.item_list = ["general",
                          "menu_minyi","menu_archive","menu_about"
                          ]
        
        self.init()
        self.update()

    def init(self):
        self.cfg = {
            "general": {
                "title": "OrgNote",
                "subtitle": "A simple org-mode blog, write blog by org-mode in Emacs",
                "author": "Leslie Zhu",
                "description":"A simple org-mode blog, write blog by org-mode in Emacs",
                "keywords":"Emacs,Blog,OrgNote,org-mode,LeslieZhu",
            },
            "menu_minyi": {
                "enable":True,
                "display-name": "MinYi"
            },
            "menu_archive": {
                "enable":True,
                "display-name": "归档"
            },                
            "menu_about": {
                "enable":True,
                "display-name": "关于"
            }
        }

    def update(self):
        import os.path
        
        self.fp.read([self.cfgfile, os.path.expanduser('~/.orgnote.ini')])
        for section in self.cfg.keys():
            for option in self.cfg[section]:
                if self.fp.has_option(section,option):
                    self.cfg[section][option] = str(self.fp.get(section,option)).strip().replace("\"","")


    def dump(self):
        self.update()
        for section in self.item_list:#self.cfg.keys():
            if not self.fp.has_section(section):
                self.fp.add_section(section)
            for option in self.cfg[section].keys():
                self.fp.set(section,option,self.cfg[section][option])

        self.fp.write(open(self.cfgfile,"w"))

    def display(self):
        """display the config.ini contents"""
        
        for key in self.item_list:#self.cfg.keys():
            print "[%s]" % key
            for item in self.cfg[key].keys():
                print "%s = %s " % (item,self.cfg[key][item])
            print
        
def main(args=None):
    cfg=Config()
    cfg.update()
    cfg.display()
    


if __name__ == "__main__":
    import sys
    sys.exit(main())
