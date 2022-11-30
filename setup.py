from setuptools import find_packages
from setuptools import setup


version = "5.0.0"

setup(
    name="plone.app.vocabularies",
    version=version,
    description="Collection of generally useful vocabularies for Plone.",
    long_description="{}\n{}".format(
        open("README.rst").read(), open("CHANGES.rst").read()
    ),
    classifiers=[
        "Development Status :: 6 - Mature",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Core",
        "Framework :: Plone :: 6.0",
        "Framework :: Zope :: 5",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="Plone Zope vocabularies",
    author="Plone Foundation",
    author_email="plone-developers@lists.sourceforge.net",
    url="https://github.com/plone/plone.app.vocabularies",
    license="GPL version 2",
    packages=find_packages(),
    namespace_packages=["plone", "plone.app"],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",
    install_requires=[
        "plone.app.querystring",
        "plone.base",
        "pytz",
        "setuptools",
        "zope.deprecation",
        "zope.globalrequest",
    ],
    extras_require=dict(
        test=[
            "mock",
            "plone.app.testing",
            "zope.configuration",
            "zope.testing",
        ]
    ),
)
