from setuptools import setup
from setuptools import find_packages
import sys
import os

version = '0.1'

setup(name='TwistedEve',
      version=version,
      description="An eavesdropping & man-in-the-middle attack tool",
      long_description=open("README.txt").read(),
      classifiers=["Framework :: Twisted",
                   "License :: OSI Approved :: GNU Affero General Public \
                   License v3"
                   ],
      keywords='mitm tls twisted proxy',
      author='Dimitris Moraitis',
      author_email='dimo@unweb.me',
      url='https://unweb.me/projects/twistedeve',
      license='AGPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
        'Twisted',
        'tlslite',
      ],
     entry_points={
         'console_scripts': [
            'twistedeve = twistedeve.main:main',
         ],
     }
     )
