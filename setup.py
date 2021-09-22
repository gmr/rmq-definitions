#!/usr/bin/env python
from os import path

import setuptools


def read_requirements(filename):
    requirements = []
    try:
        with open(path.join('requires', filename)) as req_file:
            for line in req_file:
                if '#' in line:
                    line = line[:line.index('#')]
                line = line.strip()
                if line.startswith('-r'):
                    requirements.extend(read_requirements(line[2:].strip()))
                elif line:
                    requirements.append(line)
    except IOError:
        pass
    return requirements


setuptools.setup(
    name='rmq-definitions',
    version='1.1.0',
    description=('Deterministicly sorting and formatting of RabbitMQ '
                 'definition backups'),
    author='Gavin M. Roy',
    author_email='gavinmroy@gmail.com',
    url='https://github.com/gmr/rmq-definitions',
    install_requires=read_requirements('installation.txt'),
    license='BSD',
    py_modules=['rmq_definitions'],
    entry_points={'console_scripts': [
        'rmq-definitions=rmq_definitions:main'
    ]},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: System :: Archiving :: Backup',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities'],
    test_suite='nose.collector',
    tests_require=read_requirements('testing.txt'),
    zip_safe=True
)
