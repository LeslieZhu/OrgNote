#!/usr/bin/env python
#-*- coding: utf-8 -*-

# OrgNote  ---- A simple org-mode blog, powered by python
# 
# orgnote.py ---- write blog by org-mode note
# 
# author: Leslie Zhu
# email: pythonisland@gmail.com
#
# Write note by Emacs with org-mode, and convert .org file itno .html file
# thus use orgnote.py convert into new html with speciall css
# 

from __future__ import absolute_import

def main():
    import orgnote.parser
    orgnote.parser.main()

if __name__ == "__main__":
    import sys
    sys.exit(main())
