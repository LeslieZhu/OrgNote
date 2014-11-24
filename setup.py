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

long_description = read('README.org')

setup(
    name = "orgnote",
    version = find_version("orgnote", "__init__.py"),
    keywords = ('org-mode', 'emacs','orgnote','blog'),
    description = ' A simple blog based on org-mode',
    long_description=long_description,
    license = 'GPL',


    author = 'Leslie Zhu',
    author_email = 'czhu@kdsglobal.com',
    url = 'https://github.com/LeslieZhu/OrgNote',

    packages = find_packages(),
    #package_data = {'': ['*.*'],'docs':['*.*'],'css':['*.*']},


    include_package_data = True,
    platforms = 'linux',
    zip_safe=False,

    #install_requires = ['PyYAML'],

    entry_points={
        "console_scripts": [
            "orgnote=orgnote:main",
            "orgnote%s=orgnote:main" % sys.version[:1],
            "orgnote%s=orgnote:main" % sys.version[:3],
        ],
    },
)
