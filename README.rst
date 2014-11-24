OrgNote: A simple blog based on org-mode
=======================================

Get Started
============

At first, need to fork **OrgNote** as **yourname.github.com** repository.

Thus you can open **https://yourname.github.com** in  browser after wait some minutes. 

There is a default blog now!

Post Blog
=========

Steps::

  $ git clone git@github.com:yourname/yourname.github.com.git

  $ python orgnote.py note newnote

  $ python orgnote.py page newnote

  $ python orgnote.py generate

  $ python orgnote.py server [port]

  $ git add file1 file2 ...

  $ git push origin master


`orgnote.py` Usage::

  $ python orgnote.py

    Usage:
          python orgnote.py note {notename}           ---- add a org-mode note
          python orgnote.py page {notename}           ---- convert .org to .html

          python orgnote.py generate                  ---- generate all notes
          python orgnote.py server [port]             ---- start web server for review


Configure
=========

There is only one program named `orgnote.py`, all configures will apply in this file.

basic
======

__dirs__
---------

The __dirs__ is a list() and each item is a note-list-file.

__title__
----------

The **name/title** of the blog.

__author__
-----------

The **author** of the blog.

__description__
----------------

The **description** of the blog.

__blog_keywords__
--------------------

The **keywords** of the blog.

feature
=========

note-list-file
---------------

note-list-file example::
  - [[../notes/orgnote.html][OrgNote: public   version] ]
  + [[../notes/orgnote.html][OrgNote: nopublic version] ]

Note:
- There is a space after **-/+**, this is a format of org-mode.
- If the line begins with **-**, thus the note will public to homepage of blog.
- If the line begins with **+**, thus the note will only public to =/public/nopublic.html= 

About
-------

Find the function **contain_about**, use it like::
  <p> something </p>
  

Duoshuo
-------

Find the function **duosuo**, and add http://duoshuo.com/ code into it::
  def duosuo():
      return """
      your duoshuo code here!
      """

Weibo
------

Find the function **sidebar_weibo**, and add your weibo's code into it::
  def sidebar_weibo():
      return """
             your weibo code here!
             """
Links
-------

Find the function **sidebar_link**, and add links.

Latest Blogs
-------------

Find the function **sidebar_latest**, display latest 10 notes, sample::
  def sidebar_latest(notes=list(), num=10):


The **num=10** meaning is display latest 10 notes as default.


More
=======

- `Emacs` : http://www.gnu.org/software/emacs/
- `Org-mode` : http://orgmode.org/
- sample: http://lesliezhu.github.io/

Enjoy it! :)




