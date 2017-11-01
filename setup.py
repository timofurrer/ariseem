# -*- coding: utf-8 -*-

"""
    ariseem
    ~~~~~~~

    Minimalistic REST API for wake-on-lan

    :copyright: (c) 2017 by Timo Furrer <tuxtimo@gmail.com>
    :license: MIT, see LICENSE for more details.
"""

import ast
import os
import sys
import codecs
from setuptools import setup, find_packages

#: Holds the root dir for the project.
PROJECT_ROOT = os.path.dirname(__file__)


class VersionFinder(ast.NodeVisitor):

    def __init__(self):
        self.version = None

    def visit_Assign(self, node):
        try:
            if node.targets[0].id == '__version__':
                self.version = node.value.s
        except:
            pass


def read_version():
    """Read version from __init__.py without loading any files"""
    finder = VersionFinder()
    path = os.path.join(PROJECT_ROOT, 'ariseem', '__init__.py')
    with codecs.open(path, 'r', encoding='utf-8') as fp:
        file_data = fp.read().encode('utf-8')
        finder.visit(ast.parse(file_data))

    return finder.version


#: Holds the requirements for ariseem
requirements = [
    'flask',
    'pyyaml'
]


if __name__ == '__main__':

    setup(
        name='ariseem',
        version=read_version(),
        description='Minimalistic REST API for wake-on-lan.',
        long_description='Minimalistic REST API for wake-on-lan.',
        url='http://github.com/timofurrer/colorful',
        author='Timo Furrer',
        author_email='tuxtimo@gmail.com',
        maintainer='Timo Furrer',
        maintainer_email='tuxtimo@gmail.com',
        include_package_data=True,
        packages=find_packages(exclude=['*tests*']),
        install_requires=requirements,
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'License :: OSI Approved :: MIT License',
            'Operating System :: POSIX',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: Implementation',
            'Programming Language :: Python :: Implementation :: CPython',
            'Programming Language :: Python :: Implementation :: PyPy'
        ]
    )
