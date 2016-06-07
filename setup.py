from setuptools import setup, find_packages

version = '2.3.0'

setup(
    name='plone.app.vocabularies',
    version=version,
    description="Collection of generally useful vocabularies for Plone.",
    long_description='%s\n%s' % (
        open("README.rst").read(),
        open("CHANGES.rst").read()
    ),
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 5.0",
        "Framework :: Zope2",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ],
    keywords='Plone Zope formlib vocabularies',
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
        'plone.app.imaging',
        'Products.CMFCore',
        'pytz',
        'setuptools',
        'zope.browser',
        'zope.component',
        'zope.formlib',
        'zope.i18n',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.schema',
        'zope.site',
        'Zope2',
    ],
    extras_require=dict(
        test=[
            'plone.app.testing',
            'zope.configuration',
            'zope.testing',
        ]
    ),
)
