#!/usR/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Frederic'

import sys
sys.path.append("../src")
from gehol.studentcalendar import StudentCalendar
from gehol.converters.icalwriter import convert_student_calendar_to_ical, write_ical_to_file
from pprint import pprint

DATA_FILE = "../data/student/IR_MA1_img_1_14.html"
DATA_FILE = "../data/student/SC_INFO_MA1_multimedia_1_14.html"
DATA_FILE = "../data/student/PHILO_BA1_HIST_1_14.html"

if __name__ == "__main__":
    f = open(DATA_FILE)
    cal = StudentCalendar(f)
    print cal.header_data
    pprint(cal.events)

    first_monday = '20/09/2010'
    ical_content = convert_student_calendar_to_ical(cal, first_monday)
    #print ical_content
    write_ical_to_file(ical_content, "%s.ics" % cal.description)


