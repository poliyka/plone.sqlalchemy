# -*- coding: utf-8 -*-
"""Installer for the plone.sqlalchemy package."""

from setuptools import find_packages
from setuptools import setup


long_description = '\n\n'.join([
    open('README.md').read(),
    open('CONTRIBUTORS.rst').read(),
    open('CHANGES.rst').read(),
])


setup(
    name='plone.sqlalchemy',
    version='1.0a1',
    description="Sqlalchemy in Plone",
    long_description=long_description,
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 5.2",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone CMS',
    author='poliyka',
    author_email='jkny3586@gmail.com',
    url='https://github.com/collective/plone.sqlalchemy',
    project_urls={
        'PyPI': 'https://pypi.python.org/pypi/plone.sqlalchemy',
        'Source': 'https://github.com/collective/plone.sqlalchemy',
        'Tracker': 'https://github.com/collective/plone.sqlalchemy/issues',
        # 'Documentation': 'https://plone.sqlalchemy.readthedocs.io/en/latest/',
    },
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['plone'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    python_requires="==2.7, >=3.6",

    # 需要先手動安裝
    # sudo apt install alembic
    # pip3 install zope.i18nmessageid

    # MySql
    # sudo apt install -y mysql-client
    # sudo apt-get install libmysqlclient-dev
    # sudo apt install libssl-dev
    # sudo apt install libcrypto++-dev
    # pip3 install mysqlclient

    # postgresql
    # pip3 install psycopg2-binary
    # sudo apt install libpq-dev python3-dev
    # pip3 install psycopg2
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
        'z3c.jbot',
        'plone.api>=1.8.4',
        'plone.restapi < 8.0.0',
        'plone.app.dexterity',
        'SQLAlchemy==1.4.23',
        'zope.sqlalchemy==1.5',
        'psycopg2==2.9.1',
        'mysqlclient==2.0.3',
        'sqlalchemy_mixins==1.5',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            # Plone KGS does not use this version, because it would break
            # Remove if your package shall be part of coredev.
            # plone_coredev tests as of 2016-04-01.
            'plone.testing>=5.0.0',
            'plone.app.contenttypes',
            'plone.app.robotframework[debug]',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [console_scripts]
    update_locale = plone.sqlalchemy.locales.update:update_locale
    """,
)
