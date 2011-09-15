import sys
sys.path.append("../src")

from gehol import GeholProxy
from gehol.converters.utils import write_content_to_file
from gehol.converters.rfc5545icalwriter import convert_geholcalendar_to_ical

if __name__=="__main__":
    print 'import calendar test --> csv files'
    all_courses = ['INFOH500','BIMEH404','STATH400', 'COMMB411', 'TRANH100', 'INFOH100']
    host = '164.15.72.157:8081'
    first_monday = '19/09/2011'

    gehol_proxy = GeholProxy(host)

    for course in all_courses:
        print "fetching events for course %s" % course
        cal = gehol_proxy.get_course_calendar(course)
        dest_filename = '%s.ics' % course
        ical = convert_geholcalendar_to_ical(cal, first_monday)
        print "Saving %s events to %s" % (course, dest_filename)
        ical_data = ical.as_string()
        write_content_to_file(ical_data, dest_filename)

