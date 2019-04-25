#!/usr/bin/env python2
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai

__license__   = 'GPL v3'
__copyright__ = '2019, Paul'
__docformat__ = 'restructuredtext en'

from calibre.gui2.actions import InterfaceAction
from calibre.customize import InterfaceActionBase
from calibre.gui2 import error_dialog
from calibre.utils.date import format_date
import datetime


class InterfacePluginBase(InterfaceActionBase):
    name                = 'Auto Datestamp and View'
    description         = 'Add a date stamp and view current book'
    supported_platforms = ['windows', 'osx', 'linux']
    author              = 'Paul'
    version             = (0, 0, 9)
    minimum_calibre_version = (0, 7, 53)
    actual_plugin = 'calibre_plugins.auto_datestamp_and_view:AutoDatestampAndView'

class AutoDatestampAndView(InterfaceAction):
    name = 'Auto Datestamp and View'
    action_spec = (_('Date and view book'), None, None, None)
    action_type = 'current'
    
    def genesis(self):
        self.qaction.triggered.connect(self.gui.iactions['View']._view_calibre_books)
        orig_func = self.gui.iactions['View']._view_calibre_books

        def datestamp_and_view(book_ids):
            orig_func(book_ids)
            db = self.gui.library_view.model().db
            dateformat = 'iso'
            date_column = '#lastopened'
            custom_columns = db.custom_field_keys()
            # Make sure column exists
            if date_column not in custom_columns: 
                return error_dialog(self.gui, 'Before running this plugin', 
                        'You need to create a custom Date column called %s '%date_column, show=True)
            label = db.field_metadata.key_to_label(date_column)
            # Stamp each sele
            for book_id in book_ids:
                now = datetime.datetime.now()
                viewdate = format_date(now, dateformat, assume_utc=False, as_utc=False)
                db.set_custom(book_id, viewdate, label=label, commit=True)
        # thanks to Kovid Goyal for the following line, also for Calibre in general
        self.gui.iactions['View']._view_calibre_books = datestamp_and_view
