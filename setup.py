from setuptools import setup, find_packages

setup(name='youandme',
      version='0.0.0',
      description='Unix philosophy private messages via raw pipes and metadata paranoia',
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
