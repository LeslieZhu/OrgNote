OrgNote: A simple blog based on org-mode
=======================================



.. image:: https://pypip.in/v/orgnote/badge.png
   :target: https://pypi.python.org/pypi/orgnote

.. image:: https://travis-ci.org/LeslieZhu/OrgNote.svg?branch=master
   :target: https://travis-ci.org/LeslieZhu/OrgNote

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

  $ orgnote list

  $ orgnote status

  $ orgnote publish note-name

  $ orgnote generate

  $ orgnote server [port]

  $ orgnote deploy

Usage
=======
::

   $ orgnote help

   Usage: orgnote <command>

   Commands:
   init       Create a new OrgNote folder
   new        Create a new .org post
   list       List this blog notes
   status     Status of those notes
   publish    Auto Publish a note
   generate   Generate static files
   server     Start the server
   deploy     Deploy your website
   help       Get help on a command
   version    Display version information
   
   For more help, you can check the docs:  http://lesliezhu.github.io/OrgNote/
   
OrgNote Bash Completion
=======================

see https://github.com/LeslieZhu/orgnote-bash-completion

More
=======

- `Emacs` : http://www.gnu.org/software/emacs/
- `Org-mode` : http://orgmode.org/
- sample: http://lesliezhu.github.io/

Enjoy it! :)





