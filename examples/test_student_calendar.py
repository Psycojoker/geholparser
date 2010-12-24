#!/usR/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Frederic'

import os
import sys
sys.path.append("../src")
from gehol.studentcalendar import StudentCalendar
from gehol.converters.icalwriter import convert_student_calendar_to_ical, write_ical_to_file, convert_student_calendar_to_ics_rfc5545
from pprint import pprint

DATA_DIR = "../data/student/"
DATA_FILE = "../data/student/IR_MA1_img_1_14.html"
DATA_FILE = "../data/student/SC_INFO_MA1_multimedia_1_14.html"
DATA_FILE = "../data/student/PHILO_BA1_HIST_1_14.html"


def make_ical(filename):
    f = open(filename)
    cal = StudentCalendar(f)
    print cal.header_data
    pprint(cal.events)

    first_monday = '20/09/2010'
    ical_content = convert_student_calendar_to_ics_rfc5545(cal, first_monday)
    write_ical_to_file(ical_content, "%s.ics" % cal.description)


if __name__ == "__main__":
    for f in os.listdir(DATA_DIR):
        make_ical(DATA_DIR + f)

