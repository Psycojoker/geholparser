#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Frederic'


import re
from datetime import datetime, timedelta
from BeautifulSoup import BeautifulSoup
from utils import split_weeks, convert_time
import chardet

class StudentCalendar(object):
    def __init__(self, markup):
        if self._is_file_type_object(markup):
            markup = markup.read()
        self.html_content = markup
        soup = BeautifulSoup(self.html_content, fromEncoding='iso-8859-2')
        self.header_data = {'student_profile':None, 'faculty':None}
        self.events = {}
        self._load_content_from_soup(soup)


    def _load_content_from_soup(self, soup):
        top_level_tables = soup.html.body.findAll(name="table", recursive=False)
        header, event_grid, footer, footer2 = top_level_tables

        self._load_header_data(header)
        self._load_events(event_grid)


    def _load_header_data(self, header):
        all_entries = header.findAll(name='table')
        faculty_table = all_entries[4]
        profile_table = all_entries[6]
        self.header_data['faculty'] = self._extract_data_from_header_table(faculty_table)
        self.header_data['student_profile'] = self._extract_data_from_header_table(profile_table)


    @staticmethod
    def _extract_data_from_header_table(table):
        t = table.td.getText()
        return t


    def _load_events(self, event_table):
        all_rows = event_table.findChildren('tr', recursive=False)
        weekday_rows = all_rows[1:]

        week_events = [self._load_weekday_events(weekday) for weekday in weekday_rows]
        self.events = dict(zip(["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"], week_events))


    def _load_weekday_events(self, weekday_row):
        """
        """
        # At this point we should have a bunch of <td> elements. Some cells are empty, some cells have an event in them.
        # First <td> is the weekday string, so we skip it.
        row = weekday_row.findChildren('td', recursive=False)
        all_day_slots = row[1:]

        events = [self._process_event(slot) for slot in all_day_slots if self._slot_has_event(slot)]
        return events


    def _process_event(self, object_cell):
        cell_tables = object_cell.findChildren('table', recursive=False)
        type_table, title_table, tutor_week_table = cell_tables
        course_type = type_table.tr.findChildren('td')[1].text
        course_title = title_table.tr.td.text
        children = tutor_week_table.findChildren('td')
        course_tutor = children[0].text
        course_weeks = children[2].text

        return {
            'type':course_type,
            'organizer':course_tutor,
            'title':course_title,
            'weeks':course_weeks
        }


    @staticmethod
    def _slot_has_event(slot):
        return slot.table is not None


    @staticmethod
    def _is_file_type_object(f):
        return hasattr(f, 'read')