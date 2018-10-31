from setuptools import setup

import unittest
def getTestSuites():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_main*.py')
    return test_suite

setup(name='sct',
      version='0.0.1',
      description='Short Circuit Tester',
      url='ssh://git@stash:7999/htol/sct.git',
      author='victord',
      author_email='victor.dela.cruz@amd.com',
      license='MIT',
      packages=['sct'],
      dependency_links=[
          'https://github.com/vicdelacruz/sct.git'
      ],
      test_suite='setup.getTestSuites',
      install_requires=[
          'lxml','spidev'
      ],
      zip_safe=False)
