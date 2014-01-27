Changelog
=========

1.1.1 (2014-01-27)
------------------

-

1.1.0 (2013-11-14)
------------------

- be able to include a depth value onto path query string
  [vangheem]

- Use plone.batching.
  [khink]


1.0.8 (2013-03-14)
------------------

- Fix UnicodeDecodeError on utf8-encoded Subject strings.
  [tisto]


1.0.7 (2013-01-01)
------------------

- getVocabularyValues now checks if the vocabulary utility is missing,
  if it is the utility is just ignored. This makes the module tollarant to
  missing vocabulary utilities.
  [bosim]


1.0.6 (2012-10-03)
------------------

- _relativePath handler can now walk through the site structure (not only upwards)
  _path handler respects absolute paths without leading nav_root path
  [petschki]


1.0.5 (2012-06-29)
------------------

- Date ranges now use the _betweenDates handler, which is much more forgiving
  of empty field values, defaulting to an all-encompassing date range if neither
  value is provided, an "everything after" range if only the start date is
  provided, and a min/max range if both are provided.

  Fixes http://dev.plone.org/ticket/12965
  [esteele]


1.0.4 (2012-05-07)
------------------

- Fixed i18n of "Before today" operator and
  "x items matching your search terms.".
  [vincentfretin]


1.0.3 (2012-04-15)
------------------

* Add an optional 'brains' parameter to the query builder to obtain
  results not wrapped as an IContentListing.
  [davisagli]

* Declare all dependencies in setup.py to resolve a dependeny problem in
  test setups, where the Plone stack isn't fully loaded.
  [thet]

* Add a "today" date operator
  [esteele]

* Internationalize strings in the registry.
  [davisagli]

* Change relative date searching to be "N days" string based rather than
  datetime based.
  [esteele]

* Handle empty values on relative date fields.
  [esteele]

1.0.2 (2012-02-10)
------------------

* Change the Creator field to use the correct query operation for filtering
  on the current logged in user.
  This fixes https://dev.plone.org/ticket/12052
  [jcerjak]

* Limit number of items that show up in the preview of the edit view to 25.
  If we do not limit these results all items in the query will be rendered in
  the preview which leads to problems when the collection contains > 10k
  results.
  [timo]


1.0.1 (2011-10-17)
------------------

* Ensure inactive content is only shown to users with the appropriate
  permission.


1.0 (2011-07-19)
----------------

* Initial release
