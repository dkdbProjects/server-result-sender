from setuptools import setup

setup(name='FlaskApp',
      version='0.0.1',
      description='Server part of dkdbproject',
      author='Damir Kanafeev, Dasha Borovkova',
      author_email='domir332@live.ru',
      url='http://www.python.org/sigs/distutils-sig/',
      install_requires=['Flask>=0.10.1'],
      install_requires=['Flask-MySQLdb>=0.2.0'],
      install_requires=['Flask-RESTful>=0.3.5'],
      install_requires=['utm>=0.4.0']
      install_requires=['numpy>=1.11.0']
      install_requires=['scipy>=0.17.1']
      install_requires=['scikit-learn>=0.17.1']
      install_requires=['matplotlib>=1.5.1']
     )
