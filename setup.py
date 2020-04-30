from setuptools import setup, find_packages
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

packages = find_packages(exclude=['contrib', 'docs', 'tests'])

setup(name='youandme',
      version='2.0.0',
      description='Simple private data sharing via bytearrays, Tor tunneling and metadata paranoia',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Kevin Froman',
      packages=packages,
      scripts=['src/yam/yam.py'],
      author_email='beardog@mailbox.org',
      url='http://github.com/beardog108/youandme',
      python_requires='>=3.7',
      install_requires=[
          'stem',
          'PySocks'
      ],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent"
      ]
     )
