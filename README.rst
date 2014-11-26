OrgNote: A simple blog based on org-mode
=======================================

Install
============

Install OrgNote by `pip`::
  $ pip install orgnote

Install OrgNote by `easy_install`::

  $ easy_install orgnote

Install OrgNote by source code::

  $ git clone git@github.com:LeslieZhu/OrgNote.git
  $ cd OrgNote
  $ python setup.py install


Get Started
============

At first, you should crate a **yourname.github.com.git** on `GitHub`::

  $ git clone git@github.com:yourname/yourname.github.com.git
  $ cd yourname.github.com
  $ git clone git@github.com:LeslieZhu/orgnote-theme-freemind.git theme/freemind
  $ git clone git@github.com:LeslieZhu/orgnote-emacs-el.git scripts/
  $ orgnote init


Configure
=========

update `_config.ini` ,sample::
 
  [general]
  title = OrgNote
  subtitle = OrgNote
  author = OrgNote
  description = My information
  keywords = My Blog keywords

Post Blog
==========

::
  $ orgnote new note-name

  $ orgnote page note-name

  $ orgnote generate

  $ orgnote server [port]

  $ orgnote upload

Usage
=======
::
   $ orgnote help

   Usage: orgnote [OPTIONS]

   options:

   config                    ---- init/list config file
   init                      ---- init current dir as blog root
   new  {notename}           ---- add a org-mode note
   page {notename}           ---- convert .org to .html
   generate                  ---- generate all notes
   server [port]             ---- start web server for review
   upload                    ---- upload blog to public websites,like github
   


More
=======

- `Emacs` : http://www.gnu.org/software/emacs/
- `Org-mode` : http://orgmode.org/
- sample: http://lesliezhu.github.io/

Enjoy it! :)





