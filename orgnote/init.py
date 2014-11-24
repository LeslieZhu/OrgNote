#-*- coding: utf-8 -*-

from __future__ import absolute_import


def main(args=None):
    import os
    import os.path
    
    cur_dir = os.popen("pwd").readline().strip()
    
    path_sep = os.path.sep
    orgnote_dir = os.path.abspath(os.path.dirname(__file__))
    OrgNote_dir = path_sep.join(orgnote_dir.split(path_sep)[:-1])
    
    target_list = ["theme","notes","init-orgnote.el","public","index.html"]

    for target in target_list:
        from_path = OrgNote_dir + path_sep + target
        print "init target ",target
        os.system("cp -r %s %s" % (from_path,cur_dir))
    


if __name__ == "__main__":
    import sys
    sys.exit(main())
