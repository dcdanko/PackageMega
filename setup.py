
from setuptools import setup, find_packages

setuptools.setup(
    name='PackageMega',
    version='0.1.0',
    url='https://github.com/dcdanko/PackageMega',

    author='David C. Danko',
    author_email='dcdanko@gmail.com',

    description='Simple package manager to download and keep track of biological databases.',
    long_description=open('README.rst').read(),

    packages=find_packages(),
    package_dir={'packagemega': 'packagemega'},

    install_requires=[
        'click~=6.7',
        'DataSuper~=0.10.0',
        'gimme_input~=1.0.0',
    ],

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
)
