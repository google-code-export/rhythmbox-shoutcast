## Copyright (c) 2008 Nathan R. Yergler, Creative Commons

## Permission is hereby granted, free of charge, to any person obtaining
## a copy of this software and associated documentation files (the "Software"),
## to deal in the Software without restriction, including without limitation
## the rights to use, copy, modify, merge, publish, distribute, sublicense,
## and/or sell copies of the Software, and to permit persons to whom the
## Software is furnished to do so, subject to the following conditions:

## The above copyright notice and this permission notice shall be included in
## all copies or substantial portions of the Software.

## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
## AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
## FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
## DEALINGS IN THE SOFTWARE.

import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name = "opml",
    version = "0.5",
    author = 'Nathan R. Yergler',
    author_email = 'nathan@yergler.net',
    description = 'Lightweight OPML parsing.',
    long_description = (
        read('README.txt') 
        + '\n' + 
        read('src', 'opml', 'README')
        + '\n' +
        'Download\n' + 
        '********\n'
        ),

    license = 'MIT',
    keywords = 'xml opml',
    url = 'http://wiki.creativecommons.org/Python_OPML',

    packages = ['opml'],
    package_dir = {'' : 'src'},

    # dependencies
    install_requires = ['setuptools',
                        'lxml',
                        ],

    )
