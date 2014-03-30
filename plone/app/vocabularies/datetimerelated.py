from zope.component import getUtility
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.i18nmessageid import MessageFactory

import pytz
import random

@provider(IVocabularyFactory)
def TimezonesFactory(context, query=None):
    """Vocabulary for all timezones.

      >>> from zope.component import queryUtility
      >>> from plone.app.vocabularies.tests.base import create_context

      >>> name = 'plone.app.vocabularies.Timezones'
      >>> util = queryUtility(IVocabularyFactory, name)
      >>> context = create_context()

      >>> len(util(context)) > 500
      True

      >>> util(context).by_token['Europe/Vienna'].title
      'Europe/Vienna'

    """
    tz_list = [SimpleTerm(value=it, title=it)
               for it in pytz.all_timezones
               if query is None or query.lower() in it.lower()]
    return SimpleVocabulary(tz_list)


@provider(IVocabularyFactory)
def AvailableTimezonesFactory(context, query=None):
    """Vocabulary for available timezones, as set by in the controlpanel.

    This vocabulary is based on collective.elephantvocabulary. The reason is,
    that if timezones are used in events or in user's settings and later
    retracted by the portal manager, they should still be usable for those
    objects but not selectable in forms.

    Note: after setting available_timezones, this vocabulary must be
    reinstantiated to reflect the changes.



    """
    # TODO: if the portal_timezone is not in available_timezones, also put it
    #       in AvailableTimezone vocab.
    tzvocab = getUtility(
        IVocabularyFactory,
        'plone.app.vocabularies.Timezones'
    )(context, query)
    return wrap_vocabulary(
        tzvocab,
        visible_terms_from_registry='plone.app.event.available_timezones'
    )(context)


# PLEASE NOTE: strftime %w interprets 0 as Sunday unlike the calendar module!
WEEKDAY_PREFIXES = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

@provider(IVocabularyFactory)
def WeekdaysFactory(context):
    """Vocabulary for Weekdays - full name

      >>> from zope.component import queryUtility
      >>> from plone.app.vocabularies.tests.base import create_context

      >>> name = 'plone.app.vocabularies.Weekdays'
      >>> util = queryUtility(IVocabularyFactory, name)
      >>> context = create_context()

      >>> len(util(context))
      7

      >>> util(context).by_token['0'].title
      u'weekday_mon'

    """
    _ = MessageFactory('plonelocales')
    items = []
    for idx in range(len(WEEKDAY_PREFIXES)):
        msgstr = _('weekday_{0}'.format(WEEKDAY_PREFIXES[idx]))
        items.append(SimpleTerm(idx, str(idx), msgstr))
    return SimpleVocabulary(items)


@provider(IVocabularyFactory)
def WeekdaysAbbrFactory(context):
    """Vocabulary for Weekdays - abbreviated (3 char)

      >>> from zope.component import queryUtility
      >>> from plone.app.vocabularies.tests.base import create_context

      >>> name = 'plone.app.vocabularies.WeekdaysAbbr'
      >>> util = queryUtility(IVocabularyFactory, name)
      >>> context = create_context()

      >>> len(util(context))
      7
    
    """
    _ = MessageFactory('plonelocales')
    items = []
    for idx in range(len(WEEKDAY_PREFIXES)):
        msgstr = _('weekday_{0}_abbr'.format(WEEKDAY_PREFIXES[idx]))
        items.append(SimpleTerm(idx, str(idx), msgstr))
    return SimpleVocabulary(items)


@provider(IVocabularyFactory)
def WeekdaysShortFactory(context):
    """Vocabulary for Weekdays - Short (2 char)

      >>> from zope.component import queryUtility
      >>> from plone.app.vocabularies.tests.base import create_context

      >>> name = 'plone.app.vocabularies.WeekdaysShort'
      >>> util = queryUtility(IVocabularyFactory, name)
      >>> context = create_context()

      >>> len(util(context))
      7
    
    """
    _ = MessageFactory('plonelocales')
    items = []
    for idx in range(len(WEEKDAY_PREFIXES)):
        msgstr = _('weekday_{0}_short'.format(WEEKDAY_PREFIXES[idx]))
        items.append(SimpleTerm(idx, str(idx), msgstr))
    return SimpleVocabulary(items)


MONTH_PREFIXES = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 
                  'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

@provider(IVocabularyFactory)
def MonthFactory(context):
    """Vocabulary for Month. Full name

      >>> from zope.component import queryUtility
      >>> from plone.app.vocabularies.tests.base import create_context

      >>> name = 'plone.app.vocabularies.Month'
      >>> util = queryUtility(IVocabularyFactory, name)
      >>> context = create_context()

      >>> len(util(context))
      12
    """
    _ = MessageFactory('plonelocales')
    items = []
    for idx in range(len(MONTH_PREFIXES)):
        msgstr = _('month_{0}'.format(MONTH_PREFIXES[idx]))
        items.append(SimpleTerm(idx, str(idx), msgstr))
    return SimpleVocabulary(items)

@provider(IVocabularyFactory)
def MonthAbbrFactory(context):
    """Vocabulary for Month. Abbreviated Name (3 char)

      >>> from zope.component import queryUtility
      >>> from plone.app.vocabularies.tests.base import create_context

      >>> name = 'plone.app.vocabularies.MonthAbbr'
      >>> util = queryUtility(IVocabularyFactory, name)
      >>> context = create_context()

      >>> len(util(context))
      12
    """
    _ = MessageFactory('plonelocales')
    items = []
    for idx in range(len(MONTH_PREFIXES)):
        msgstr = _('month_{0}_abbr'.format(MONTH_PREFIXES[idx]))
        items.append(SimpleTerm(idx, str(idx), msgstr))
    return SimpleVocabulary(items)

