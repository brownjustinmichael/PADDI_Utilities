from setuptools import setup
import os

scripts = [os.path.join (root, file) for root, subdirs, files in os.walk ("scripts") for file in files if (file [0] != '.' and file [-3:] == ".py")]

setup(name='paddi_utils',
      version='0.1',
      description='A set of utilities for analyzing and running the fluid code PADDI',
      url='https://github.com/brownjustinmichael/PADDI-Utilities',
      author='Justin Brown',
      author_email='jumbrown@ucsc.edu',
      license='MIT',
      packages=['paddi_utils'],
      install_requires=["matplotlib","sqlalchemy","numpy","pandas","celery"],
      scripts=scripts,
      zip_safe=False)