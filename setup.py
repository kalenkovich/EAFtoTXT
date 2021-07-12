from setuptools import setup, find_packages

setup(
    name='eaf2txt',
    version='0.1.0',
    packages=find_packages(include=['eaf2txt', 'eaf2txt.*']),
    entry_points={
        'console_scripts': ['eaf2txt=eaf2txt.cli:main']
    },
)
