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
        


def config_init():
    """
    create _config.ini file as configure file
    """
    import os
    import os.path

    if not os.path.exists("./_config.ini"):
        print "[info] init config file"
        cur_dir = os.popen("pwd").readline().strip()
        path_sep = os.path.sep
        orgnote_dir = os.path.abspath(os.path.dirname(__file__))
        OrgNote_dir = path_sep.join(orgnote_dir.split(path_sep)[:-1])
        cmd = "cp %s/_config.ini ./_config.ini" % orgnote_dir
        os.system(cmd)
        
def main(args=None):
    config_init()
    
    


if __name__ == "__main__":
    import sys
    sys.exit(main())
