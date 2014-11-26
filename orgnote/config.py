#-*- coding: utf-8 -*-

from __future__ import absolute_import

import ConfigParser

class Config(object):
    def __init__(self,cfgfile="_config.ini"):
        self.cfgfile = cfgfile
        self.fp = ConfigParser.ConfigParser()
        self.cfg = dict()
        
        self.init()

    def init(self):
        self.cfg["title"] = ""
        self.cfg["subtitle"] = ""
        self.cfg["author"] = ""
        self.cfg["description"] = ""
        self.cfg["keywords"] = ""

    def update(self):
        self.fp.read(self.cfgfile)
        section = "general"
        if self.fp.has_section(section):
            for option in self.fp.options(section):
                self.cfg[option] = self.fp.get(section,option)
        
def main(args=None):
    cfg=Config()
    cfg.update()
    


if __name__ == "__main__":
    import sys
    sys.exit(main())
