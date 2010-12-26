import sys
sys.path.append("../src")

from gehol import GeholProxy
from gehol.converters.csvwriter import export_csv, to_csv


if __name__=="__main__":
    print 'import calendar test --> csv files'
    all_courses = ['INFOH500','BIMEH404','STATH400', 'COMMB411']
    host = '164.15.72.157:8080'
    first_monday = '20/09/2010'

    gehol_proxy = GeholProxy(host)

    for course in all_courses:
        print "fetching events for course %s" % course
        cal = gehol_proxy.get_course_calendar(course)
        dest_filename = 'agenda_%s.csv' % course
        print "Saving %s events to %s" % (course, dest_filename)
        csv_string = to_csv(cal.metadata, cal.events, first_monday)
        export_csv(cal.metadata, cal.events, dest_filename, first_monday)
