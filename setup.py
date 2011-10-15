from setuptools import setup
import sys
sys.path.append('./src')

import gehol

setup(name='gehol',
      package_dir={'': 'src'},
      packages=['gehol', 'gehol.converters'],
      version=gehol.__version__,

      #PyPI metadata
      url=['http://bitbucket.org/odebeir/ulbcalendar2cvs'],
      keywords=['calendar csv'],
      platforms='All',
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Programming Language :: Python",
        "Topic :: Software Development",
        "Topic :: Utilities"])
