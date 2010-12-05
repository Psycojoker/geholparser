from setuptools import setup
import sys
sys.path.append('./src')

import gehol

setup(name='gehol',
      package_dir={'': 'src'},
      packages=['gehol'],
      version=gehol.__version__,
      #PyPI metadata
      url=['http://bitbucket.org/odebeir/ulbcalendar2cvs'],
      keywords=['calendar csv'],
      platforms='All')
