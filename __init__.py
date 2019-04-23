#!/usr/bin/env python2
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai

__license__   = 'GPL v3'
__copyright__ = '2019, Paul'
__docformat__ = 'restructuredtext en'

from calibre.gui2.actions import InterfaceAction
from calibre.customize import InterfaceActionBase
from calibre.ebooks.metadata.book.base import Metadata
from calibre.gui2 import error_dialog, info_dialog, question_dialog
from calibre.utils.date import format_date
import datetime

class InterfacePluginBase(InterfaceActionBase):
    name                = 'Datestamp and View'
    description         = 'Add a date stamp and view current book'
    supported_platforms = ['windows', 'osx', 'linux']
    author              = 'Paul'
    version             = (0, 0, 7)
    minimum_calibre_version = (0, 7, 53)
    actual_plugin = 'calibre_plugins.datestamp_and_view:DatestampAndView'

class DatestampAndView(InterfaceAction):
    name = 'Datestamp and View'
    action_spec = (_('Date and view book'), None, None, _("r"))
    action_type = 'current'

    def genesis(self):
        self.qaction.triggered.connect(self.stamp)
        self.stamp_menu = self.qaction.menu()

    def stamp(self):
        db = self.gui.library_view.model().db
        date_column = '#lastopened'
        custom_columns = db.custom_field_keys()
        # Make sure column exists
        if date_column not in custom_columns: 
            return error_dialog(self.gui, 'Before running this plugin', 'You need to create a custom Date column called %s '%date_column, show=True)
        label = db.field_metadata.key_to_label(date_column)
        # Get selected row(s)
        rows = self.gui.library_view.selectionModel().selectedRows()
        if not rows or len(rows) == 0:
            return error_dialog(self.gui, 'Cannot view', 'No books selected', show=True)
        # Map the rows to book ids
        book_ids = list(map(self.gui.library_view.model().id, rows))
        for book_id in book_ids:
            dateformat = 'yyyy-MM-dd hh:mm:ss'
            now = datetime.datetime.now()
            viewdate = format_date(now, dateformat, assume_utc=False, as_utc=False)
            db.set_custom(book_id, viewdate, label=label, commit=True)
        # Now view the book(s)
        self.gui.iactions['View'].view_book(self)


