from setuptools import setup, find_packages
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(name='youandme',
      version='0.0.0',
      description='Simple private data sharing via bytearrays, Tor tunneling and metadata paranoia',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Kevin Froman',
      author_email='beardog@mailbox.org',
      url='https://chaoswebs.net',
      extras_require={
        "tor":  ["stem>=1.8"],
      },
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent"
      ]
     )
