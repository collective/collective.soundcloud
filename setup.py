from setuptools import setup, find_packages
import sys, os

version = '1.0a-dev'
shortdesc = 'Soundcloud integration for Plone'
longdesc =  open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()  
longdesc += open(os.path.join(os.path.dirname(__file__), 'HISTORY.rst')).read()  
longdesc += open(os.path.join(os.path.dirname(__file__), 'LICENSE.rst')).read()  

setup(name='collective.soundcloud',
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
      package_dir = {'': 'src'},
      namespace_packages=[],
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'setuptools',
          'Plone',
          'plone.app.dexterity',
          'collective.autopermission',            
          'yafowil.zope2',
          'yafowil.yaml',
          'soundcloudapi',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
