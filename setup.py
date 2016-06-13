# 1. change (increase) version id in `setup.py`
# 1.2 install locally: pip install --upgrade .
# 2. python setup.py sdist register upload

from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding

with open('README.rst') as f:
    readme = f.read()

setup(
    name='checktype',
    version='1.1.7',
    description='Intuitive and minimalistic type checking for Python objects',
    long_description=readme,
    url='https://github.com/renaud/checktype',
    author='Renaud Richardet',
    author_email='renaud@apache.org',
    license='Apache License (2.0)',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
         'Operating System :: OS Independent',
         'Environment :: Console',
    ],
    keywords='type checking',
    py_modules=['checktype']
)
