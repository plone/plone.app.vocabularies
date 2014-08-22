Overview
========

A collection of generally useful vocabularies.


Common Named Vocabularies
=========================

* plone.app.vocabularies.AvailableContentLanguages
* plone.app.vocabularies.SupportedContentLanguages
* plone.app.vocabularies.Roles
* plone.app.vocabularies.Groups
* plone.app.vocabularies.AllowedContentTypes
* plone.app.vocabularies.AllowableContentTypes
* plone.app.vocabularies.PortalTypes
* plone.app.vocabularies.ReallyUserFriendlyTypes
* plone.app.vocabularies.UserFriendlyTypes
* plone.app.vocabularies.Skins
* plone.app.vocabularies.Workflows
* plone.app.vocabularies.WorkflowStates
* plone.app.vocabularies.WorkflowTransitions
* plone.app.vocabularies.AvailableEditors
* plone.app.vocabularies.Keywords
* plone.app.vocabularies.SyndicationFeedTypes
* plone.app.vocabularies.SyndicatableFeedItems
* plone.app.vocabularies.Users
* plone.app.vocabularies.Catalog


Date/Time Related Vocabularies
==============================

``plone.app.vocabularies.Timezones``
    all timezones provided by ``pytz``

``plone.app.vocabularies.CommonTimezones``
    common timezones provided by ``pytz``. This are those
    a user would choose from and is not too much confused.

``plone.app.vocabularies.AvailableTimezones``
    timezones configured in the portal.

``plone.app.vocabularies.Weekdays``
    the seven weekdays in fullname. Value is the day number start counting
    at zero on monday. Title of the term is an i18n messagestring in
    ``plonelocales`` namespace, so it translates.

``plone.app.vocabularies.WeekdaysAbbr``
   same as above but with 3 character abbreviations.

``plone.app.vocabularies.WeekdaysShort``
   same as above but with 2 character abbreviations.

``plone.app.vocabularies.Month``
   same as above but with month names starting with zero in january.

``plone.app.vocabularies.MonthAbbr``
   same as above but with 3 character abbreviations.

