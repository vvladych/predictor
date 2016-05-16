from setuptools import setup, find_packages

__author__ = "vvladych"
__date__ = "$30.12.2015 23:12:01$"

setup (
  name = 'predictor',
  version = '0.1',
  packages = find_packages(),
  install_requires=['psycopg2', 'gi'],
  author = 'vvladych',
  author_email = '',
  summary = 'Predictions management',
  url = '',
  license = '',
  long_description= 'Predictions',
  # could also include long_description, download_url, classifiers, etc.
)
