"""
OrgNote  ---- A simple org-mode blog, write blog by org-mode in Emacs

author: Leslie Zhu
email: pythonisland@gmail.com

Write note by Emacs with org-mode, and convert .org file into .html file,
then use orgnote convert into new html with default theme.
"""

from __future__ import absolute_import

__version__ = "1.0.7"

def main():
    import orgnote.__main__
    orgnote.__main__.main()
