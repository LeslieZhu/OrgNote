#-*- coding: utf-8 -*-

from __future__ import absolute_import


def config_init():
    import os
    import os.path

    print "[info] init config file"
    cur_dir = os.popen("pwd").readline().strip()
    path_sep = os.path.sep
    orgnote_dir = os.path.abspath(os.path.dirname(__file__))
    OrgNote_dir = path_sep.join(orgnote_dir.split(path_sep)[:-1])
    os.system("cp %s/_config.py %s/_config.py" % (orgnote_dir,OrgNote_dir))

def main(args=None):
    
    print "Config...."
    


if __name__ == "__main__":
    import sys
    sys.exit(main())
