"""PackageMega -- package manager for biological databases."""

import os
import sys

from setuptools import setup, find_packages
from setuptools.command.install import install


version = {}
VERSION_PATH = os.path.dirname(os.path.realpath(__file__))
with open('{0}/packagemega/version.py'.format(VERSION_PATH)) as fp:
    exec(fp.read(), version)


with open('README.rst') as readme_file:
    readme = readme_file.read()


requirements = [
    'click~=6.7',
    'DataSuper~=0.10.0',
    'gimme_input~=1.0.0',
    'PyYAML==3.12',  # pinned version required by yaml_backed_structs
    'yaml_backed_structs~=0.9.0',
]


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version."""

    description = 'Verify that the git tag matches our version.'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != 'v{0}'.format(version['__version__']):
            info = 'Git tag: {0} does not match the version of this app: {1}'
            info = info.format(tag, version['__version__'])
            sys.exit(info)


setup(
    name='PackageMega',
    version=version['__version__'],
    url='https://github.com/dcdanko/PackageMega',

    author=version['__author__'],
    author_email=version['__email__'],

    description='Simple package manager to download and keep track of biological databases.',
    long_description=readme,

    packages=find_packages(),
    install_requires=requirements,

    entry_points={
        'console_scripts': [
            'packagemega=packagemega.cli:main'
        ]
    },

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    cmdclass={
        'verify': VerifyVersionCommand,
    },
)
