from setuptools import setup

setup(name='sct',
      version='0.0.1',
      description='Short Circuit Tester',
      url='ssh://git@stash:7999/htol/sct.git',
      author='victord',
      author_email='victor.dela.cruz@amd.com',
      license='MIT',
      packages=['src'],
      dependency_links=[
          'https://github.com/vicdelacruz/sct.git'
      ],
      install_requires=[
          'lxml','spidev'
      ],
      zip_safe=False)
