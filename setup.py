"""Packaging settings."""

from codecs import open
from os.path import abspath, dirname, join
from subprocess import call

from setuptools import Command, find_packages, setup

from rbcore import __version__


this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.rst'), encoding='utf-8') as file:
    long_description = file.read()


class RunTests(Command):
    """Run all tests."""
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run all tests!"""
        errno = call(['py.test', '--cov=simple_backup', '--cov-report=term-missing'])
        raise SystemExit(errno)

setup(
    name = 'Radio Bretzel core',
    version = __version__,
    description = 'Radio Bretzel core app. Make your own webradios !',
    long_description = long_description,
    url = 'https://source.radiobretzel.org/app/rb-core',
    author = "Radio Bretzel Org",
    author_email = "radiobretzel@ntymail.com",
    license = "None",
    classifiers = [
        'Intended Audience :: System Administrators',
        'Topic :: Music Streaming',
        'Licence :: None (Public domain ?)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords = 'webradio, sharing, music, chat, rooms',
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires = [
        'Flask',
        'Flask-pymongo',
        'cerberus',
    ],
    extras_require = {
        'docker': ['docker'],
        'test': ['Flask-Testing']
    },
    entry_points = {
    },
    cmdclass = {'test': RunTests},
)
