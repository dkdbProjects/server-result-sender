#!/usr/bin/python

from setuptools import setup

setup(name='FlaskApp',
      version='0.0.1',
      description='Server part of dkdbproject',
      author='Damir Kanafeev, Dasha Borovkova',
      author_email='domir332@live.ru',
      url='http://www.python.org/sigs/distutils-sig/',
      install_requires=['Flask>=0.10.1',
                        'Flask-MySQLdb>=0.2.0',
                        'Flask-RESTful>=0.3.5',
                        'utm>=0.4.0',
                        'scikit-learn>=0.17.1'
      ]
     )
