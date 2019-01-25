import sys
from codecs import open
from os.path import abspath, dirname, join
from subprocess import call

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand


this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()


class PyTests(TestCommand):
    """Run all tests."""
    description = 'run tests'
    user_options = [("pytest-args=", "a", "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ""

    def finalize_options(self):
        pass

    def run(self):
        import shlex
        # import here, cause outside the eggs aren't loaded
        import pytest

        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


install_requires = [
    'appdirs',
    'cerberus',
    'docker',
    'Flask',
    'Flask-PyMongo',
    'pyyaml'
]

tests_require = [
    'Flask-Testing',
    'pylint',
    'pytest'
]

extras_require = {
    'test': tests_require
}


setup(
    name='Radio Bretzel core',
    version='0.2.0',
    description='Radio Bretzel core app. Make your own webradios !',
    long_description=long_description,
    url='https://source.radiobretzel.org/app/rb-core',
    author="Radio Bretzel Org",
    author_email="radiobretzel@ntymail.com",
    license="None",
    classifiers=[
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
    keywords='webradio, sharing, music, chat, rooms',
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require=extras_require,
    entry_points={
        'console_scripts': [
            'rb-core=rbcore.cli:main'
        ]
    },
    cmdclass={'pytest': PyTests},
)
