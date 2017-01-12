# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup


version = '4.0.1'

setup(
    name='plone.app.vocabularies',
    version=version,
    description='Collection of generally useful vocabularies for Plone.',
    long_description='{0}\n{1}'.format(
        open('README.rst').read(),
        open('CHANGES.rst').read()
    ),
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: 5.0',
        'Framework :: Plone :: 5.1',
        'Framework :: Zope2',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='Plone Zope vocabularies',
    author='Plone Foundation',
    author_email='plone-developers@lists.sourceforge.net',
    url='https://github.com/plone/plone.app.vocabularies',
    license='GPL version 2',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['plone', 'plone.app'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Acquisition',
        'plone.app.querystring',
        'Products.CMFCore',
        'pytz',
        'setuptools',
        'zope.browser',
        'zope.component',
        'zope.i18n',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.schema',
        'zope.site',
        'Zope2',
    ],
    extras_require=dict(
        test=[
            'mock',
            'plone.app.testing',
            'zope.configuration',
            'zope.testing',
        ]
    ),
)
