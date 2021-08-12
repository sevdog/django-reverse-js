#!/usr/bin/env python
from setuptools import setup, find_packages


setup(
    name='django-reverse-js',
    version='0.1.0',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Framework :: Django',
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
    ],
    license='MIT',
    description='Javascript url handling for Django that doesn\'t hurt.',
    author='Davide Setti',
    url='https://github.com/sevdog/django-reverse-js',
    download_url='http://pypi.python.org/pypi/django-reverse-js/',
    packages=find_packages(),
    package_data={
        'django_reverse_js': [
            'templates/django_reverse_js/*',
        ]
    },
    install_requires=[
        'Django>=2.2',
    ]
)
