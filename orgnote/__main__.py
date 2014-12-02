#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
OrgNote  ---- A simple org-mode blog, write blog by org-mode in Emacs

author: Leslie Zhu
email: pythonisland@gmail.com

Write note by Emacs with org-mode, and convert .org file into .html file,
then use orgnote convert into new html with default theme.
"""

from __future__ import absolute_import

def main():
    import orgnote.parser
    orgnote.parser.main()

if __name__ == "__main__":
    import sys
    sys.exit(main())
