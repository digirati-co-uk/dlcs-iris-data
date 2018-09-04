#!/usr/bin/env python

from distutils.core import setup

setup(name='dlcs-iris-data',
      version='0',
      description='DLCS Iris session data library',
      author='Digirati Ltd',
      packages=['dlcs_iris_data',],
      license='MIT',
      install_requires=[
          'iris-data==0'
      ],
      dependency_links=[
              'git+https://github.com/digirati-co-uk/iris-data.git#egg=iris-data-0',
      ],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python 3',
          'Programming Language :: Python 3 :: Only',
          'License :: OSI Approved :: MIT License',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ]
      )
