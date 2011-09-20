#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Frederic'

import os
import sys
sys.path.append("../src")
from gehol import GeholProxy
from gehol.professorcalendar import ProfessorCalendar
from gehol.converters.utils import  write_content_to_file
from gehol.converters.rfc5545icalwriter import convert_geholcalendar_to_ical
from pprint import pprint



first_monday = '19/09/2011'

def make_ical_from_local_file(filename):
    f = open(filename)
    cal = ProfessorCalendar(f)
    print cal.header_data
    pprint(cal.events)

    ical_content = convert_geholcalendar_to_ical(cal, first_monday)
    write_content_to_file(ical_content, "%s.ics" % cal.description)


def make_ical_from_prof_id(prof_id):
    gehol_proxy = GeholProxy()
    cal = gehol_proxy.get_professor_calendar(prof_id, "1-14")
    ical = convert_geholcalendar_to_ical(cal, first_monday)
    ical_data = ical.as_string()
    outfile = "%s.ics" % ical.name
    print "writing ical file : %s" % outfile
    write_content_to_file(ical_data, outfile)



PROF_IDS = [32781, 49171, 55405, 20453]


if __name__ == "__main__":
    for id in PROF_IDS:
        make_ical_from_prof_id(id)