#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Frederic'

import os
import sys
sys.path.append("../src")
from gehol import GeholProxy
from gehol.studentcalendar import StudentCalendar
from gehol.converters.utils import  write_content_to_file
from gehol.converters.rfc5545icalwriter import convert_calendar_to_ical
from pprint import pprint

DATA_DIR = "../data/student/"
DATA_FILE = "../data/student/IR_MA1_img_1_14.html"
DATA_FILE = "../data/student/SC_INFO_MA1_multimedia_1_14.html"
DATA_FILE = "../data/student/PHILO_BA1_HIST_1_14.html"

first_monday = '20/09/2010'

def make_ical_from_local_file(filename):
    f = open(filename)
    cal = StudentCalendar(f)
    print cal.header_data
    pprint(cal.events)

    ical_content = convert_calendar_to_ical(cal, first_monday)
    write_content_to_file(ical_content, "%s.ics" % cal.description)


URLs = [("MA1 en sciences informatiques - Spécialisée - Multimedia", "http://164.15.72.157:8080/Reporting/Individual;Student%20Set%20Groups;id;%23SPLUS0FACD0?&template=Ann%E9e%20d%27%E9tude&weeks=1-14&days=1-6&periods=5-33&width=0&height=0"),
        ("BA1 en sciences de l'ingénieur, orientation ingénieur civil - Série 2B", "http://164.15.72.157:8080/Reporting/Individual;Student%20Set%20Groups;id;%23SPLUSA6299F?&template=Ann%E9e%20d%27%E9tude&weeks=1-14&days=1-6&periods=5-33&width=0&height=0"),
        ("BA3 en information et communication", "http://164.15.72.157:8080/Reporting/Individual;Student%20Set%20Groups;id;%23SPLUS35F074?&template=Ann%E9e%20d%27%E9tude&weeks=1-14&days=1-6&periods=5-33&width=0&height=0"),
]


def make_ical_from_url(name, url):
    gehol_proxy = GeholProxy()
    cal = gehol_proxy.get_student_calendar_from_url(url)
    ical_data = convert_calendar_to_ical(cal, first_monday)
    outfile = "%s.ics" % name
    print "writing ical file : %s" % outfile
    write_content_to_file(ical_data, outfile)


if __name__ == "__main__":
    for (profile, url) in URLs:
        make_ical_from_url(profile, url)
