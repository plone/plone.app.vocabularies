Changelog
=========

.. You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst

.. towncrier release notes start

5.0.2 (2023-04-06)
------------------

Bug fixes:


- Import navigation root specific from plone.base.
  And so remove transitive circular dependency on plone.app.layout.
  [jensens] (#74)


5.0.1 (2023-03-22)
------------------

Internal:


- Update configuration files.
  [plone devs] (b2d5d4a5)


5.0.0 (2022-11-30)
------------------

Bug fixes:


- Final release.
  [gforcada] (#600)


5.0.0b1 (2022-08-31)
--------------------

New features:


- Remove dependency on CMFPlone (use plone.base).
  In images vocab use utility instead of import.
  isort/black (pure) and pyupgrade --py37-plus`.
  Remove traces of six.
  Bump version to 5.0.
  [jensens] (#72)


4.3.0 (2021-09-01)
------------------

New features:


- Add new ``StaticCatalogVocabulary`` class providing a simplified mechanism for
  creating queryable content vocabularies. Allows use of e.g. AJAXSelectWidget for
  fields that store Relations or UUIDs. (#66)


4.2.2 (2021-02-16)
------------------

Bug fixes:


- Change vocabulary tokens to use ``base64.urlsafe_b64encode()``.
  No newlines and safe to use as an xml attribute.
  See `community post <https://community.plone.org/t/tags-subject-field-mangling-long-terms/13067>`_.
  [flipmcf] (#64)


4.2.1 (2020-09-26)
------------------

Bug fixes:


- Fixed deprecation warning for zope.site.hooks. (#3130)


4.2.0 (2020-06-30)
------------------

New features:


- Add new plone.app.vocabularies.MetadataFields vocabulary.
  [vincentfretin] (#62)


4.1.2 (2020-04-20)
------------------

Bug fixes:


- Minor packaging updates. (#1)


4.1.1 (2019-08-29)
------------------

Bug fixes:


- Principals vocabularies: Fixed handling of results from multiple PAS plugins (like pasldap and mutable_properties). (#60)


4.1.0 (2019-04-29)
------------------

New features:


- Overhaul of the groups-vocabulary ``plone.app.vocabularies.Groups``,
  a refined version of the users-vocabulary ``plone.app.vocabularies.Users``,
  a new principals vocabulary combining users and groups ``plone.app.vocabularies.Principals``.
  Ability to apply a filter to the vocabularies in subclasses.
  Moved all to ``principals.py``, bbb import are in place (``user.py``, ``security,py``).
  Deprecated the ``UserSource`` and ``GroupsSource`` implementations.
  Documented new vocabulary in ``README.rst``.
  Move doctests to unittests and added more tests.
  Benefits:
  200x faster validation of groups;
  less and cleaner code;
  unified code for all three vocabularies.
  [jensens] (#56)


4.0.7 (2018-09-27)
------------------

Bug fixes:

- Python 3 support [ale-rt, pbauer]


4.0.6 (2018-02-11)
------------------

Bug fixes:

- Do not wake up all the users when no query is submitted
  [ale-rt]


4.0.5 (2018-02-05)
------------------

Bug fixes:

- Fix test that breaks when catalog is not registered as a utility in CMF 2.3+
  [pbauer]

- Add Python 2 / 3 compatibility
  [vincero]


4.0.4 (2017-07-03)
------------------

Bug fixes:

- Let ``plone.app.vocabularies.SupportedContentLanguages`` return the language title in native language.
  [thet]

- Remove unittest2 dependency
  [kakshay21]


4.0.3 (2017-05-10)
------------------

Bug fixes:

- return empty vocabulary when no imagescales defined
  [fgrcon]


4.0.2 (2017-03-29)
------------------

Bug fixes:

- plone/Products.CMFPlone#1794: use permissive vocabulary type
  for numeric-indexed weekday and month vocabularies
  to avoid breaking GenericSetup import.
  [seanupton]

- plone/Products.CMFPlone#1268: use permissive vocabulary type
  for ReallyUserFriendlyTypes, to avoid insertion of new types
  in plone.displayed_types (registry) from breaking GenericSetup
  profiles in add-ons.
  [seanupton]


4.0.1 (2017-01-12)
------------------

Bug fixes:

- Fix problem in ParseError fallback introduced in 4.0
  [jensens]


4.0 (2016-11-17)
----------------

Breaking changes:

- Make zope.formlib optional.
  [gforcada]

- Mark vocabularies based on zope.formlib as deprecated.
  [gforcada]

Bug fixes:

- Adapt code to follow Plone styleguide.
  [gforcada]

- Fix in catalog: If ZCTextIndex catches a ParseError, try w/o SearchableText if there is one given.
  Often ``Query contains only common words`` happen (only stop words given) and results are not fetched.
  Semantically this means that we want all results.
  [jensens]

3.0 (2016-06-12)
----------------

Breaking changes:

- CatalogVocabulary now takes a query for it's constructor instead of a LazyMap of brains
  and lazy loads terms. Also, in __contains__, do a UID query instead of checking the
  entire contents of the result. This prevents potential DOS with custom code where the
  whole contents of the catalog would get loaded with terms created for it on every
  validation attempt.
  [vangheem]

New features:

- Optional allow to filter keyword vocabulary to a current *section* based on the current context.
  The class was build for easy subclassing - and still is.
  It allows to override the section fetching logic in a subclass.
  The default logic is first to look in the controlpanel if there is a ``IEditingSchema.subjects_of_navigation_root`` boolean.
  If its ``True`` the ``getNavigationRootObject`` is used as the section and only keywords used in this section are part of the vocabulary.
  Otherwise all keywords in the index are displayed.
  [jensens]


2.3.0 (2016-06-07)
------------------

New features:

- Refactor ``KeywordsVocabulary`` logic of term construction from  *dirty* values out into own functions.
  Document functions in README.
  [jensens]


2.2.5 (2016-05-25)
------------------

Bug fixes:

- Import getAllowedSizes from CMFPlone to avoid dependency on plone.app.imaging.
  [davisagli]

- Fix bug where queries would not be parsed correctly for date queries on the catalog
  vocabulary
  [vangheem]


2.2.4 (2016-04-26)
------------------

New:

- Add ImagesScales vocabulary.
  [bsuttor]

Fixes:

- increase readability of code in CatalogSource.
  [jensens]


2.2.3 (2016-03-03)
------------------

New:

- Vocabulary for permissions
  [ebrehault]

- Vocabulary for portal action categories
  [ebrehault]


2.2.2 (2016-02-25)
------------------

Fixes:

- Restrict Catalog vocabulary to search current Navigation Root unless
  path is specified.
  [alecm]


2.2.1 (2015-12-03)
------------------

Fixes:

- Make user vocabulary handle non-ASCII characters.
  This fixes https://github.com/plone/plone.app.widgets/issues/120
  [davisagli]


2.2.0 (2015-10-28)
------------------

Fixes:

- Updated version to 2.2.0, as the previous release introduced an
  incompatibility with Plone 4.3.
  [maurits]

- Pull default_charset value from the configuration registry.
  [esteele]


2.1.21 (2015-09-07)
-------------------

- Pull available_editors values from the configuration registry.
  [esteele]


2.1.20 (2015-08-13)
-------------------

- Cleanup: PEP8, decorators for zca, et al. Also pimped the README.
  [jensens]


2.1.19 (2015-07-29)
-------------------

- Fixed SyndicatableFeedItems to allow unicode characters in objects titles.
  [Gagaro]


2.1.18 (2015-06-05)
-------------------

- change CatalogSource to be able to validate
  path strings in addition to UIDs
  [vangheem]


2.1.17 (2015-05-13)
-------------------

- default to having english with AvailableContentLanguageVocabularyFactory
  to fix issue that happens sometimes when setting language and multilingual
  is not installed
  [vangheem]

- Fix issue with missing context in plone.app.vocabularies.Users.
  [pbauer]


2.1.16 (2014-09-07)
-------------------

- Added the missing Authenticated and Anonymous roles within the
  `RolesVocabulary``.
  [ichim-david]

- Cleanup.
  [thet]


2.1.15 (2014-04-11)
-------------------

- Make ``KeywordsVocabulary`` more customizable using an ``keyword_index``
  class variable to allow users to inherit and just override that attribute
  to build their own keyword vocabularies.
  [saily]

- Add datetime related vocabularies: timezones, weekdays, months.
  This are moved from ``plone.app.event`` and extended by to be more
  complete.
  [yenzenz]

- Add catalog source which can eventually replace the vocabulary.
  [davisagli]


2.1.14 (2014-02-23)
-------------------

- Add actions vocabulary.
  [giacomos]


2.1.13 (2014-01-27)
-------------------

-

2.1.12 (2013-11-14)
-------------------

- provide proper contains method for catalog results
  [vangheem]

- fallback to getSite for grabbing portal_catalog
  [vangheem]

- catalog vocabulary query could be None
  [garbas]

- getTerm and getTermByToken were not really checking if item is in the
  vocabulary list
  [garbas]

- use sort_on and sort_order in catalog vocabulary
  [vangheem]

2.1.11 (2013-07-18)
-------------------

- Add documentation to SlicableVocabulary, fix handling of internal structure
  [do3cc]

- SlicableVocabulary context is not needed when initialing
  [garbas]

- KeywordsVocabularyFactory now accepts query which filters keywords listed in vocabulary
  [garbas]

- add support for a catalog vocabulary
  [vangheem]


2.1.10 (2013-01-30)
-------------------

- UsersVocabulary should search on fullname .
  [garbas]


2.1.9 (2013-01-13)
------------------

- adding users vocabulary (lazy loading of users) also supports searching over
  users.
  [garbas]


2.1.8 (2012-10-03)
------------------

- Make KeywordsVocabulary work with unicode and non-unicode vocabularies.
  [thet]

- Fix exceptions with workflow states/transitions titles when their titles
  contained encoded characters [ericof]

- Fix exception with workflow vocabulary when workflow titles contained UTF-8 encoded
  characters [miohtama]

- Add syndication feed types vocabulary
  [vangheem]


2.1.7 (2012-07-02)
------------------

- Depend on zope.formlib instead of zope.app.form.
  [davisagli]

- Remove hard dependency on Archetypes.
  [davisagli]

2.1.6 (2012-04-09)
------------------

- Made our mock queryUtility in the tests more life like.  This avoids
  test failures in combination with zope.pagetemplate 3.6.0 or higher.
  [maurits]


2.1.5 - 2011-12-22
------------------

- Ensure that the keywords vocabulary term titles are unicode values,
  as per zope.schema.interfaces.ITitledTokenizedTerm.
  [mj]


2.1.4 - 2011-12-22
------------------

- Ensure that the keywords vocabulary term tokens are 7-bit values,
  as per zope.schema.interfaces.ITokenizedTerm.
  [mj]


2.1.3 - 2011-07-04
------------------

- Roles vocabulary is translated and sorted by translated role id.
  Fixes http://dev.plone.org/plone/ticket/11958.
  [WouterVH]


2.1.2 - 2011-04-21
------------------

- Types vocabularies are sorted by translated titles.
  [thomasdesvenain]

- Add MANIFEST.in.
  [WouterVH]

- Transitions vocabulary is translated and sorted by transition id.
  [thomasdesvenain]


2.1.1 - 2011-03-02
------------------

- Exclude 'text/x-plone-outputfilters-html' from the allowable content types
  vocabulary.
  [davisagli]


2.1 - 2011-02-10
----------------

- Remove "Discussion Item" from BAD_TYPES vocabulary.
  [timo]


2.0.2 - 2010-10-27
------------------

- Translation of workflow states vocabularies didn't work in some contexts.
  [thomasdesvenain]


2.0.1 - 2010-07-18
------------------

- Update license to GPL version 2 only.
  [hannosch]


2.0 - 2010-07-01
----------------

- Internationalized editor label (especially for 'None' value).
  [thomasdesvenain]


2.0b4 - 2010-06-13
------------------

- Use the standard libraries doctest module.
  [hannosch]


2.0b3 - 2010-04-07
------------------

- Add a vocabulary to list all Keywords (via the Subject index).
  [esteele]

- Avoid ConstraintNotSatisfied-error when GS-importing the default navigation
  portlet. Fixes https://dev.plone.org/plone/ticket/8380
  [WouterVH]


2.0b2 - 2010-01-24
------------------

- In the skins vocabulary, give the 'Plone Default' skin the title '(Unstyled)'
  to reduce confusion, now that Sunburst is actually the default.
  [davisagli]


2.0b1 - 2009-12-27
------------------

- Added missing zope.browser dependency.
  [hannosch]


2.0a2 - 2009-12-16
------------------

- Avoid the last use of ``SimpleVocabulary.fromItems``. This refs
  http://dev.plone.org/plone/ticket/6480.
  [hannosch]

- Removed funky Acquisition handling for vocabularies inside addforms. This
  closes http://dev.plone.org/plone/ticket/9408.
  [hannosch]


2.0a1 - 2009-11-14
------------------

- Avoid dependencies on zope.app.pagetemplate and zope.app.schema.
  [hannosch]

- Added AvailableEditors vocabulary.
  [robgietema]

- Removed ChangeSet from the BAD_TYPES as this is not a portal type anymore.
  [maurits]

- Use the ITerms interface from the new zope.browser package.
  [hannosch]

- Specified package dependencies.
  [hannosch]


1.0.6 - 2008-11-06
------------------

- Made the tests forward-compatible with Python 2.6.
  [hannosch]

- The QuerySearchableTextSourceView made terms with string titles. However
  zope.app.form.browser.source assumes it to be unicode, with the result that
  you get unicode errors if you have non-ascii characters. [regebro]


1.0.5 - 2008-08-18
------------------

- Documentation updates.
  [hannosch]


1.0.4 - 2008-03-09
------------------

- Added option to omit the current folder in a browse query, this is used
  for the UberSelectionWidget.
  [fschulze]


1.0.3 - 2008-02-13
------------------

- Added tests for the catalog, groups and users sources. Fixed three bugs,
  where a LookupError was not raised.
  [hannosch]

- Added tests for the special term classes.
  [hannosch]

- Added tests for the language, security, skins, types and
  workflow vocabularies.
  [hannosch]


1.0.2 - 2007-12-24
------------------

- Fixed invalid context argument passed into the translation machinery in
  the workflow state vocabulary. This fixes
  http://dev.plone.org/plone/ticket/7492.
  [hannosch]

- Added optional default query string to searchable text source.
  [fschulze]

- Correct name for attributes.
  [wichert]


1.0.1 - 2007-08-17
------------------

- Fixed catalog vocabulary when dealing with the degenerate-case of
  an empty value. This makes it work better with the UberSelectionWidget.
  [optilude]

- Made catalog vocabulary less fragile for simple/short queries.
  [optilude]


1.0 - 2007-08-14
----------------

- Fixed ReallyUserFriendlyTypesVocabulary to include the Messages for
  type names. This refs http://dev.plone.org/plone/ticket/6911.
  [hannosch]


1.0rc3 - 2007-07-28
-------------------

- Fixed missing history.
  [hannosch]


1.0rc2 - 2007-07-27
-------------------

- Fixed to return localized workflow state names.
  [deo]


1.0rc1 - 2007-07-09
-------------------

- Added new ReallyUserFriendlyTypes and a BAD_TYPES list, which are used
  to filter out types which are not content types at all.
  [hannosch]

- Added new AvailableContentLanguages and SupportedContentLanguages
  vocabularies.
  [hannosch]

- If we have a users vocabulary, we should have a groups one :)
  [optilude]

- Make use of description-aware terms
  [optilude]

- Allow parameterisation of the query, so that we can restrict to
  folders-only, for example.
  [optilude]

- Add a user source, so that we can use the UberSelectionWidget on users.
  [optilude]


1.0b3 - 2007-05-1
-----------------

- Back to getToolByName we go.
  [wichert]


1.0b2 - 2007-03-23
------------------

- Replaced getToolByName with getUtility.
  [hannosch]


1.0b1 - 2007-03-05
------------------

- Added workflow vocabulary.
  [optilude]

- Added UserFriendlyTypes vocabulary.
  [hannosch]


1.0a2 - 2007-02-06
------------------

- Some initial vocabularies.
  [hannosch, optilude]

- Initial package structure.
  [zopeskel]
