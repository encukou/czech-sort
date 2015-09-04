import os
import sys
import io

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def finalize_options(self):
        super().finalize_options()
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

tests_require = ['pytest']

with io.open('README', encoding='utf-8') as f:
    long_description = f.read()

setup_args = dict(
    name='czech-sort',
    version='0.1',
    packages=['czech_sort'],

    description="""Text sorting function for the Czech language""",
    long_description=long_description,
    author='Petr Viktorin',
    author_email='encukou@gmail.com',
    url='https://github.com/encukou/czech-sort',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],

    install_requires=[],

    extras_require={
        'test': tests_require,
    },

    tests_require=tests_require,
    cmdclass={'test': PyTest},
)


if __name__ == '__main__':
    setup(**setup_args)
