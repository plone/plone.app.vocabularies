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
    user of the portal (searchable)

``plone.app.vocabularies.Groups``
    groups of the portal (searchable)

``plone.app.vocabularies.Roles``
    all possible roles in the portal

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
    All Subjects aka Tags aka Keywords used by the portals content


``plone.app.vocabularies.Catalog``
    Generic queryable catalog


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
   same as above but with month names starting with zero in january.

``plone.app.vocabularies.MonthAbbr``
   same as above but with 3 character abbreviations.

Images
------

``plone.app.vocabularies.ImagesScales``
   All image scales which are avaiable on Plone site.


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
    Token is encoed carefully and Title converted to unicode.

``plone.app.vocabularies.terms.safe_simplevocabulary_from_values`` (function)
    Create a ``SimpleVocabulary`` from a iterable (list) of *dirty* or *untrusted* values.
    Utilizes above ``safe_simpleterm_from_value`` to achieve this.


Source Code
===========

Contributors please read the document `Process for Plone core's development <http://docs.plone.org/develop/plone-coredev/index.html>`_

Sources are at the `Plone code repository hosted at Github <https://github.com/plone/plone.app.vocabularies>`_.
