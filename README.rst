OrgNote: A simple blog based on org-mode
=======================================

.. image:: https://img.shields.io/pypi/v/orgnote.svg
   :target: https://pypi.python.org/pypi/orgnote

.. image:: https://img.shields.io/pypi/dm/orgnote.svg
   :target: https://pypi.python.org/pypi/orgnote
                       
.. image:: https://readthedocs.org/projects/orgnote/badge/?version=latest
   :target: http://orgnote.readthedocs.org/zh_CN/latest/

.. image:: https://travis-ci.org/LeslieZhu/OrgNote.svg?branch=master
   :target: https://travis-ci.org/LeslieZhu/OrgNote

.. image:: https://badges.gitter.im/LeslieZhu/OrgNote.svg
   :alt: Join the chat at https://gitter.im/LeslieZhu/OrgNote
   :target: https://gitter.im/LeslieZhu/OrgNote?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
         

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

update `_config.yml` ,sample::
 
  # OrgNote Configuration
  ## Docs: http://lesliezhu.github.io/OrgNote/
  ## Source: https://github.com/LeslieZhu/OrgNote

  # Site
  title: OrgNote
  subtitle: "A simple org-mode blog, write blog by org-mode in Emacs"

  author: OrgNote
  email: pythonisland@gmail.com
  
  language: zh-CN
  
  # About this blog
  description: "Use OrgNote."
  keywords: "OrgNote,Emacs,org-mode,blog,python,geek"

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
   
   For more help, you can check the docs:  http://orgnote.readthedocs.org/zh_CN/latest/

Emacs Version
==============

Tested via ``GNU Emacs 24.4.1``

Docs
=======

see http://orgnote.readthedocs.org/zh_CN/latest/
   
OrgNote Bash Completion
=======================

see https://github.com/LeslieZhu/orgnote-bash-completion

More
=======

- `Emacs` : http://www.gnu.org/software/emacs/
- `Org-mode` : http://orgmode.org/
- sample: http://lesliezhu.github.io/

Enjoy it! :)
