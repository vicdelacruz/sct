from setuptools import setup, find_namespace_packages

import unittest

def getTestSuites():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test*.py')
    return test_suite

setup(name='sct',
      version='0.0.1',
      description='Short Circuit Tester',
      url='ssh://git@stash:7999/htol/sct.git',
      author='victord',
      author_email='victor.dela.cruz@amd.com',
      license='MIT',
      packages=find_namespace_packages(include=['sct.*']),
      package_dir={'sct':'sct'},
      dependency_links=[
          'https://github.com/vicdelacruz/sct.git'
      ],
      test_suite='setup.getTestSuites',
      install_requires=[
          'lxml','spidev'
      ],
      entry_points={
          'console_scripts': ['sct=sct:main'],
      },
      include_package_data=True,
      zip_safe=False,
)
