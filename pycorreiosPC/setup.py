#!/usr/bin/env python

import os
import glob
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

datadir = os.path.join('sounds')
datafiles = [(datadir, [f for f in glob.glob(os.path.join(datadir, '*'))])]

setup(
    name="pycorreios",
    version="1.0",
    author="Eduardo dos Santos Pereira",
    author_email="pereira.somoza@gmail.com",
    description=("Sistema de Alerta de Entregas Correios"),
    license="GNU v3",
    keywords="correios, alerta",
    url="https://github.com/duducosmos/pylatex2doc",
    install_requires=['easygui', 'pygame'],
    py_modules = ['pycorreios', 'pycorreiosUI', 'pycorreios_qt',
                  'pycorreioscmd', 'BeautifulSoup'],
    long_description=read('README'),
    packages= find_packages(),
    package_data={'': ['*.wav', '*.gif']},
    data_files= datafiles,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: GNU V3",
    ],
    entry_points = {"console_scripts":
                    ["pycorreios = pycorreioscmd:main",
                    "pycorreios_qt = pycorreios_qt:main", ]},
)
