"""Packaging settings."""


from codecs import open
from os.path import abspath, dirname, join
from subprocess import call

from setuptools import Command, find_packages, setup

from fsyncer import __version__


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
        errno = call(['py.test', '--cov=syncer', '--cov-report=term-missing'])
        raise SystemExit(errno)


setup(
    name = 'fsyncer',
    version = __version__,
    description = 'Keep your repositories up-to-date all the time.',
    long_description = 'Keep your repositories up-to-date all the time.',
    url = 'https://github.com/Skarlso/fsyncer',
    author = 'Gergely Brautigam',
    author_email = 'gergely.brautigam@gmail.com',
    license = 'LICENSE',
    classifiers = [
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords = 'cli,git',
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires = ['docopt'],
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    entry_points = {
        'console_scripts': [
            'fsyncer=fsyncer.cli:main',
        ],
    },
    cmdclass = {'test': RunTests},
)