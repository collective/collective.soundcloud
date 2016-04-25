# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup
import os

version = '1.0a-dev'
shortdesc = 'Soundcloud Integration for Plone'
longdesc = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
longdesc += open(os.path.join(os.path.dirname(__file__), 'HISTORY.rst')).read()
longdesc += open(os.path.join(os.path.dirname(__file__), 'LICENSE.rst')).read()

setup(
    name='collective.soundcloud',
    version=version,
    description=shortdesc,
    long_description=longdesc,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development',
        "Framework :: Plone",
    ],
    keywords='',
    author='Jens Klein    ',
    author_email='jens@bluedynamics.com',
    url=u'http://github.com/collective/collective.soundcloud',
    license='GPLv2',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['collective'],
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'Plone',
        'plone.app.async',
        'setuptools',
        'soundcloudapi',
        'yafowil.plone',
        'yafowil.yaml',
    ],
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
