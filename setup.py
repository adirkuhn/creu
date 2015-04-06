from setuptools import setup
from model import db

setup(name='creu',
      version='1.0',
      description='web crawler and api for techcrunch news',
      author='Adir Kuhn',
      author_email='adirkuhn@gmail.com',
      url='http://www.python.org/sigs/distutils-sig/',
      install_requires=['Flask>=0.10.1', 'MarkupSafe', 'Flask-SQLAlchemy==1.0', 'lxml==3.4.2'],
     )

#create db
db.create_all()