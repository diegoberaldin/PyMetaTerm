# -*- coding: utf-8 -*-

"""
.. currentmodule:: src.model.itemmodels.entry

This module contains the ``QtCore.QAbstractItemModel`` subclass that is used
to represent the collection of entries stored in the currently opened termbase.
This model is the basis on top of which the entry list in the user interface is
built and allows to access to entries via model indexes as well as extracting
the lemma of the vedette term for each entry depending on the main language
that has been selected for display.
"""

from PyQt4 import QtCore


class EntryModel(QtCore.QAbstractListModel):
    """High level representation of the list of the entries that belong to the
    currently opened termbase, which is of little use except for the views that
    are connected to it.
    """

    def __init__(self, termbase):
        """Constructor method.

        :param termbase: reference to the currently opened termbase
        :type termbase: Termbase
        :rtype: EntryModel
        """
        super(EntryModel, self).__init__()
        self._entries = termbase.entries
        self._language = None

    @property
    def language(self):
        """Returns a reference to the main display language, i.e. the language
        in which the entries (at least their vedette terms for the language) are
        displayed in the user interface.

        :returns: locale of the selected main language
        :rtype: str
        """
        return self._language

    @language.setter
    def language(self, value):
        """Changes the main display language to the given value. Such a change
        invalidates the model since all displayed entries must update their
        lemma to the one of the vedette term for the new language.

        :param value: new locale of the main language
        :type value: str
        :rtype: None
        """
        self._language = value
        self.modelReset.emit()

    def rowCount(self, parent=QtCore.QModelIndex(), *args, **kwargs):
        """Calculates the number of rows (children) of the given index, which
        in this case, being a flat model, corresponds to the number of items
        that are contained in the internal entry list.

        :param parent: index whose child number must be determined
        :returns: the number of children of the given index
        :rtype: int
        """
        return len(self._entries)

    def data(self, index=QtCore.QModelIndex(), role=QtCore.Qt.DisplayRole):
        """Allows view to access the data that are stored inside the model by
        converting the index to the proper object.

        :param index: reference to the model index being accessed
        :type index: QtCore.QModelIndex
        :param role: role the view is trying to access with
        :type role: int
        :returns: a graphical representation of the model data
        :rtype: object
        """
        if index.isValid():
            entry = self.get_entry(index)
            if role == QtCore.Qt.DisplayRole:
                return entry.get_vedette(self.language)

    def get_entry(self, index):
        """Returns the (data access) Entry object that corresponds to the given
        index in the invocation model.

        :param index: index that identifies the entry within the model
        :type index: QtCore.QModelIndex
        :returns: a reference to the Entry corresponding to the given index
        :rtype: Entry
        """
        if index.row() < self.rowCount():
            return self._entries[index.row()]
