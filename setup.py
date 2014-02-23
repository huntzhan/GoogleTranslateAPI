#!/usr/bin/env python

from setuptools import setup

setup(
    name='google_translate_api',
    version='0.2.1',
    author='Zhan Haoxun',
    author_email='programmer.zhx@gmail.com',

    url='https://github.com/haoxun/GoogleTranslateAPI',
    license='MIT',
    description='API of google translation service.',
    long_description=open('README.rst').read(),

    install_requires=['requests', 'futures'],
    py_modules=['google_translate_api'],
    test_suite='test_google_translate_api',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
)
