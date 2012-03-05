from setuptools import setup
from setuptools import find_packages
import sys
import os

version = '0.2'

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
        'tlslite==0.3.9dev',
      ],
      dependency_links=[
        'https://nodeload.github.com/d-mo/tlslite/tarball/master#egg=tlslite-0.3.9dev',
      ],
     entry_points={
         'console_scripts': [
            'twistedeve = twistedeve.main:main',
         ],
     }
     )
