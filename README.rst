Overview
========

A collection of generally useful vocabularies for Plone.

It is implemented using ``zope.schema.vocabulary``.
Intended to be used as a base and example for custom vocabularies.


Common Named Vocabularies
=========================

Languages
---------

``plone.app.vocabularies.AvailableContentLanguages``
    all known languages

``plone.app.vocabularies.SupportedContentLanguages``
    currently configured/supported content languages for the portal


Users, Groups, Security
-----------------------

``plone.app.vocabularies.Users``
    Users of the portal (searchable).

``plone.app.vocabularies.Groups``
    Groups of the portal (searchable).

``plone.app.vocabularies.Principals``
    Combined groups and users of the portal (searchable).
    Values are prefixed by ``group:...`` or ``user:...``.

The factory-class of the above three vocabularies is made for subclassing to filter the results in the subclass.
The post-filtering approach works by overriding the ``def use_principal_triple(self, principal_triple):`` method of the ``plone.app.vocabularies.principals.BaseFactory`` subclass.
``use_principal_triple`` argument ``principal_triple`` is a triple ``(value, token, title)``.
``use_principal_triple`` is expected to return ``True`` when the triple has be added to the vocabulary or ``False`` if it has to be skipped.
Be aware there might be many values, like several thousands, in the vocabulary and the filtering has to be perform.
The subclass needs to have a ``source`` attribute with value one out of ``user``, ``group`` or ``principal``.
Don't forget to register the new vocabulary in ZCML!

``plone.app.vocabularies.Roles``
    all possible roles in the portal

``plone.app.vocabularies.Permissions``
    all possible permissions in the portal

Text Input Field
----------------

``plone.app.vocabularies.AllowedContentTypes``
    Configured allowed mime-types (text/\*) for text input fields

``plone.app.vocabularies.AllowableContentTypes``
    All possible mime types (text/\*) for text input fields

``plone.app.vocabularies.AvailableEditors``
    Configured WYSIWIG editors


Portal Types
------------

``plone.app.vocabularies.PortalTypes``
    All portal-types installed in the portal

``plone.app.vocabularies.ReallyUserFriendlyTypes``
    Static filtered list of portal-types.
    Filter is a list of portal_type ids (strings) defined at ``plone.app.vocabularies.types.BAD_TYPES``.

``plone.app.vocabularies.UserFriendlyTypes``
    Portal types filtered as 'user friendly' by the Types Tool.


Portal actions
--------------

``plone.app.vocabularies.Actions``
    All the actions category ids. Used in Actions portlet.

``plone.app.vocabularies.PortalActionCategories``
    All the actions categories (ids + translated title). Used in Actions control panel.


Workflows
---------

``plone.app.vocabularies.Workflows``
    All installed workflows

``plone.app.vocabularies.WorkflowStates``
    All titles of workflow states - for any workflow installed

``plone.app.vocabularies.WorkflowTransitions``
    All titles of workflow transitions - for any workflow installed


Syndication/ Feeds
------------------

``plone.app.vocabularies.SyndicationFeedTypes``
    Configured allowed feed types

``plone.app.vocabularies.SyndicatableFeedItems``
    Folders or Collections on the first two navigation levels (depth=2) relative to the site root.
    Value is UID of the Folder or Collection, term is title of it
    (searchable)


Catalog
-------

``plone.app.vocabularies.Keywords``
    It either displays all Subjects aka Tags aka Keywords used by the portals content.
    Or if there is a ``IEditingSchema.subjects_of_navigation_root`` boolean set to True in the registry,
    the ``getNavigationRootObject`` is used as the section and only keywords used in this section are part of the vocabulary.

    Developers can subclass ``plone.app.vocabularies.catalog.KeywordVocabulary``, it is build to be developer friendly.
    ``keyword_index`` property may be redefined to use a different index than 'Subject' for the Keywords.
    ``path_index`` property may be redefined to use a different index than ``path`` for the sections path
    ``section`` method may be redefined to located the section keywords should be restricted to.

``plone.app.vocabularies.Catalog``
    Generic queryable catalog

``plone.app.vocabularies.MetadataFields``
    List of available metadata fields (catalog brain columns) that can be used
    as table columns in a folder or collection listing.


Theme
-----

``plone.app.vocabularies.Skins``
    Themes/ skins available in the portal.


Date/Time Related
-----------------

``plone.app.vocabularies.Timezones``
    all timezones provided by `pytz <http://pythonhosted.org/pytz/>`_

``plone.app.vocabularies.CommonTimezones``
    common timezones provided by 'pytz'.
    This are those a user would choose from and is not too much confused.

``plone.app.vocabularies.AvailableTimezones``
    timezones configured in the portal.

``plone.app.vocabularies.Weekdays``
    the seven weekdays in fullname.
    Value is the day number start counting at zero on monday.
    Title of the term is an i18n messagestring in ``plonelocales`` namespace, so it translates.

``plone.app.vocabularies.WeekdaysAbbr``
   same as above but with 3 character abbreviations.

``plone.app.vocabularies.WeekdaysShort``
   same as above but with 2 character abbreviations.

``plone.app.vocabularies.Month``
   same as above but with month names starting with zero in January.

``plone.app.vocabularies.MonthAbbr``
   same as above but with 3 character abbreviations.

Images
------

``plone.app.vocabularies.ImagesScales``
   All image scales which are available on Plone site.


API/ Tools
==========

``plone.app.vocabularies.terms.TermWithDescription`` (class)
    A SimpleTerm accepting additionally a description parameter.
    Like title it may be used for display.

``plone.app.vocabularies.terms.BrowsableTerm`` (class)
    A term which may be browsed.
    In a vocabulary those are used to identify terms which are actually browsable (e.g. those representing folders).

``plone.app.vocabularies.terms.safe_simpleterm_from_value`` (function)
    Create a ``SimpleTerm`` from a *dirty* or *untrusted* value.
    Token is encoded carefully and Title converted to Unicode.

``plone.app.vocabularies.terms.safe_simplevocabulary_from_values`` (function)
    Create a ``SimpleVocabulary`` from a iterable (list) of *dirty* or *untrusted* values.
    Utilizes above ``safe_simpleterm_from_value`` to achieve this.


Source Code
===========

Contributors please read the document `Process for Plone core's development <https://docs.plone.org/develop/coredev/docs/index.html>`_

Sources are at the `Plone code repository hosted at Github <https://github.com/plone/plone.app.vocabularies>`_.
