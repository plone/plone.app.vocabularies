from setuptools import setup, find_packages

version = '2.1.12'

setup(
    name='plone.app.vocabularies',
    version=version,
    description="A collection of generally useful vocabularies.",
    long_description='%s\n%s' % (
        open("README.rst").read(),
        open("CHANGES.rst").read()
    ),
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Zope2",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
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
    extras_require=dict(
        test=[
            'zope.configuration',
            'zope.testing',
            'Products.PloneTestCase',
        ]
    ),
    install_requires=[
        'setuptools',
        'zope.browser',
        'zope.component',
        'zope.formlib',
        'zope.i18n',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.schema',
        'zope.site',
        'Acquisition',
        'Products.CMFCore',
        'Zope2',
        'plone.app.querystring'
    ],
)
