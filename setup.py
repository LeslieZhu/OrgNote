import codecs
import os
import sys
import re

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    return codecs.open(os.path.join(here, *parts), 'r').read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

#long_description = read('DESCRIPTION.rst')
long_description = """
Quick Started
==============


At first, you should crate a **yourname.github.com.git** on **GitHub**::

  $ git clone git@github.com:yourname/yourname.github.com.git
  $ cd yourname.github.com
  $ orgnote init

Thus, update **_config.yml** configure file.



Usage
======

The usage of **orgnote**::

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
"""

setup(
    name = "orgnote",
    version = find_version("orgnote", "__init__.py"),
    keywords = ('org-mode', 'emacs','orgnote','blog'),
    description = ' A simple blog based on org-mode',
    long_description=long_description,
    license = 'GPL',


    author = 'Leslie Zhu',
    author_email = 'pythonisland@gmail.com',
    url = 'https://github.com/LeslieZhu/OrgNote',

    packages = find_packages(),
    package_dir = {'orgnote':'orgnote',
               },
                   
    package_data = {
        '': ['*.py'],
        '':['_config.yml'],
        '':['DESCRIPTION.rst']
    },


    include_package_data = True,
    platforms = 'linux',
    zip_safe=False,

    #tests_require=['pytest'],

    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
    ],
    
    entry_points={
        "console_scripts": [
            "orgnote=orgnote:main",
            "orgnote%s=orgnote:main" % sys.version[:1],
            "orgnote%s=orgnote:main" % sys.version[:3],
        ],
    },

    install_requires = [
        "PyYAML==3.11",
	"Pygments==2.1.3",
	"beautifulsoup4==4.4.1",
	"bs4==0.0.1",
    ]

    #extras_require={
    #    'testing': ['pytest'],
    #}
    
)
