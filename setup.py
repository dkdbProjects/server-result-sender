from setuptools import setup

setup(name='FlaskApp',
      version='1.0',
      description='A basic Flask app with static files',
      author='Ryan Jarvinen',
      author_email='ryanj@redhat.com',
      url='http://www.python.org/sigs/distutils-sig/',
      install_requires=['Flask>=0.10.1'],
      install_requires=['Flask-MySQLdb>=0.2.0'],
      install_requires=['Flask-RESTful>=0.3.5'],
      install_requires=['utm>=0.4.0']
     )
