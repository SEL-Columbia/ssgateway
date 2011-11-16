import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'pyyaml',
    'colander',
    'WTForms',
    'nose',
    'coverage',
    'sqlalchemy-migrate',
    'SQLAlchemy',
    'simplejson',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'pyramid_beaker',
    'zope.sqlalchemy',
    ]

if sys.version_info[:3] < (2, 5, 0):
    requires.append('pysqlite')

setup(name='ssgateway',
      version='0.0',
      description='ssgateway',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='ssgateway',
      install_requires=requires,
      entry_points="""\

      [console_scripts]
      export-table = ssgateway.commands:export_table
      import-table = ssgateway.commands:import_table
      run-message  = ssgateway.commands:run_message

      [paste.app_factory]
      main = ssgateway:main
      """,
      paster_plugins=['pyramid'],
      )
