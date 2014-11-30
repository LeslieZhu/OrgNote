#-*- coding: utf-8 -*-

from __future__ import absolute_import

import ConfigParser

class Config(object):
    def __init__(self,cfgfile="_config.ini"):
        self.cfgfile = cfgfile
        self.fp = ConfigParser.ConfigParser()
        self.fp.optionxform = str
        self.cfg = dict()
        
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
            
            }

    def update(self):
        import os.path
        
        self.fp.read([self.cfgfile, os.path.expanduser('~/.orgnote.ini')])
        for section in self.cfg.keys():
            for option in self.cfg[section]:
                if self.fp.has_option(section,option):
                    self.cfg[section][option] = str(self.fp.get(section,option)).strip().replace("\"","")


    def dump(self):
        print "dump ini"
        self.update()
        for section in self.cfg.keys():
            if not self.fp.has_section(section):
                self.fp.add_section(section)
            for option in self.cfg[section].keys():
                self.fp.set(section,option,self.cfg[section][option])

        self.fp.write(open(self.cfgfile,"w"))
        
def main(args=None):
    cfg=Config()
    cfg.update()
    


if __name__ == "__main__":
    import sys
    sys.exit(main())
