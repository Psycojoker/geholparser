#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Frederic'

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
        # Take only the first 3 top-level tables. Sometimes the html is broken and we don't get the 4th.
        # We also don't get the closing tags. This piece of software is pretty brilliant
        header, event_grid, footer = top_level_tables[:3]

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

        # get the column labels, save as actual hours objects
        hours_row = all_rows[0].findChildren('td', recursive=False)
        hours = [convert_time(hour_col.text) for hour_col in hours_row[1:]]

        # get the events for each day
        weekday_rows = all_rows[1:]
        week_events = [self._load_weekday_events(weekday_data, day, hours) for (day,weekday_data) in enumerate(weekday_rows)]
        self.events = week_events


    def _load_weekday_events(self, weekday_row, day, hours):
        """
        """
        # At this point we should have a bunch of <td> elements. Some cells are empty, some cells have an event in them.
        # First <td> is the weekday string, so we skip it.
        row = weekday_row.findChildren('td', recursive=False)
        all_day_slots = row[1:]

        events = []
        current_time_idx = 0
        for time_slot in all_day_slots:
            if self._slot_has_event(time_slot):
                new_event = self._process_event(time_slot, hours[current_time_idx])
                events.append(new_event)
                current_time_idx += new_event['num_timeslots']
            else:
                current_time_idx += 1
                
        return events


    def _process_event(self, object_cell, starting_hour):
        num_timeslots = int(object_cell['colspan'])
        cell_tables = object_cell.findChildren('table', recursive=False)
        # event box : 3 tables, one per line :
        #   - location/course type 
        #   - title
        #   - tutor/weeks
        location_type_table, title_table, tutor_weeks_table = cell_tables

        location = location_type_table.tr.findChildren('td')[0].text
        course_type = location_type_table.tr.findChildren('td')[1].text

        course_title = title_table.tr.td.text

        children = tutor_weeks_table.findChildren('td')
        course_tutor = children[0].text
        course_weeks = children[2].text

        return {
            'type':course_type,
            'location':location,
            'organizer':course_tutor,
            'title':course_title,
            'weeks':split_weeks(course_weeks),
            'num_timeslots':num_timeslots,
            'start_time':starting_hour,
            'stop_time':starting_hour + timedelta(hours = self._convert_num_timeslots_to_hours(num_timeslots))
        }

    @staticmethod
    def _convert_num_timeslots_to_hours(num_timeslots):
        # 1 timeslot = 30 minutes
        return float(num_timeslots / 2)

    @staticmethod
    def _slot_has_event(slot):
        return slot.table is not None


    @staticmethod
    def _is_file_type_object(f):
        return hasattr(f, 'read')