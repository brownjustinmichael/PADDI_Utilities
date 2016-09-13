from setuptools import setup
import os
import sys
import shutil

import numpy as np

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

# clean previous build
for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        if (name.startswith("compressed") and not(name.endswith(".pyx") or name.endswith(".pxd"))):
            os.remove(os.path.join(root, name))
    for name in dirs:
        if (name == "build"):
            shutil.rmtree(name)

scripts = [os.path.join (root, file) for root, subdirs, files in os.walk ("scripts") for file in files if (file [0] != '.' and file [-3:] == ".py")]

setup(name='paddi_utils',
      version='0.1',
      description='A set of utilities for analyzing and running the fluid code PADDI',
      url='https://github.com/brownjustinmichael/PADDI-Utilities',
      author='Justin Brown',
      author_email='jumbrown@ucsc.edu',
      license='MIT',
      packages=['paddi_utils'],
      install_requires=["matplotlib","sqlalchemy","numpy","pandas","celery","f90nml","cython"],
      scripts=scripts,
      zip_safe=False,
      cmdclass = {'build_ext': build_ext},
      include_dirs = [np.get_include()],
      ext_modules = [
          Extension("paddi_utils.data.compressed", 
                    sources=["paddi_utils/data/compressed.pyx"],
                    libraries=["jc", "jpeg12"],
                    extra_link_args=["-L./extern/jutils/", "-L./extern/jutils/jpeg12/"]
               )
          ]
      )