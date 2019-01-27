import sys
from codecs import open
from os.path import abspath, dirname, join
from subprocess import call

from setuptools import find_packages, setup

this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()



INSTALL_REQUIREMENTS = [
    'appdirs',
    'cerberus',
    'docker',
    'Flask',
    'Flask-PyMongo',
    'pyyaml'
]

TEST_REQUIREMENTS = [
    'Flask-Testing',
    'pylint',
    'pytest'
]

EXTRA_REQUIREMENTS = {
    'test': TEST_REQUIREMENTS
}


setup(
    name='Radio Bretzel core',
    version='0.3.0',
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
    install_requires=INSTALL_REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS,
    extras_require=EXTRA_REQUIREMENTS,
    entry_points={
        'console_scripts': [
            'rb-core=rbcore.cli:main'
        ]
    },
)
