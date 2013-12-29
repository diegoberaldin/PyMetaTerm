# -*- coding: utf-8 -*-

"""
.. currentmodule:: src.controller.entry

"""

from src.controller.abstract import AbstractController
from src import model as mdl


class EntryController(AbstractController):
    def __init__(self, entry_model, entry_view):
        super(EntryController, self).__init__()
        self._model = entry_model
        self._view = entry_view
        # sets the language of the entry model
        self._model.language = self._view.entry_list.current_language

    def _handle_language_changed(self):
        self._model.language = self._view.entry_list.current_language

    def _handle_new_entry(self):
        self._view.entry_display.display_create_entry_form()

    def _handle_save_entry(self):
        form = self._view.entry_display.content
        if form.is_new:
            # creates the new entry
            entry = mdl.get_main_model().open_termbase.create_entry()
            # inserts all terms
            for (locale, lemmata) in form.get_terms().items():
                assert len(lemmata) == 1
                lemma = lemmata.pop()
                entry.add_term(lemma, locale, True)
        else:  # manipulating an existing entry
            entry = form.entry
        for (property_id,
             value) in form.get_entry_level_property_values().items():
            # inserts entry-level properties
            entry.set_property(property_id, value)
        for ((language_id, property_id),
             value) in form.get_language_level_property_values().items():
            # insert language-level properties
            entry.set_language_property(language_id, property_id, value)

        for ((locale, lemma, property_id),
             value) in form.get_term_level_property_values().items():
            # inserts term properties
            term = entry.get_term(locale, lemma)
            term.set_property(property_id, value)
        # updates the entry model
        if form.is_new:
            self._model.add_entry(entry)
        else:
            self._model.update_entry(entry)
        # updates the UI
        self._view.entry_display.display_entry(entry)

    def _handle_entry_index_changed(self, index):
        selected_entry = self._model.get_entry(index)
        self._view.entry_display.display_entry(selected_entry)

    def _handle_edit_entry(self):
        entry = self._view.entry_display.current_entry
        self._view.entry_display.display_update_entry_form(entry)

    def _handle_delete_entry(self):
        entry = self._view.entry_display.current_entry
        mdl.get_main_model().open_termbase.delete_entry(entry)
        self._model.delete_entry(entry)
        self._view.entry_display.display_welcome_screen()
