Overhaul of the groups-vocabulary ``plone.app.vocabularies.Groups``,
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
[jensens]