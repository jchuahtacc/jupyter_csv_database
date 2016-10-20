# -*- coding: utf-8 -*-
from __future__ import print_function
from setuptools import setup
try:
    from jupyterpip import cmdclass
except:
    import pip, importlib
    pip.main(['install', 'jupyter-pip']); cmdclass = importlib.import_module('jupyterpip').cmdclass

setup(
    name='neesdb',
    version='0.1.1',
    description='',
    author='',
    author_email='',
    license='',
    url='https://github.com/jchuahtacc/jupyter_nees_database',
    keywords='python ipython javascript widget mywidget jupyter',
    classifiers=['Development Status :: 4 - Beta',
                 'Programming Language :: Python',
                 'License :: OSI Approved :: MIT License'],
    packages=['neesdb'],
    include_package_data=True,
    install_requires=["jupyter-pip"],
    cmdclass=cmdclass('neesdb'),
)
