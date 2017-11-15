import setuptools

setuptools.setup(
    name="PackageMega",
    version="0.1.0",
    url="https://github.com/dcdanko/PackageMega",

    author="David C. Danko",
    author_email="dcdanko@gmail.com",

    description="Simple package manager to download and keep track of biological databases",
    long_description=open('README.rst').read(),

    packages=['packagemega'],
    package_dir={'packagemega': 'packagemega'},

    install_requires=[
        'click==6.7',
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
