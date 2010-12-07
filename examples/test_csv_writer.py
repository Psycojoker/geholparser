import sys
sys.path.append("../src")

from gehol.coursecalendar import CourseCalendar
from gehol.csvwriter import export_csv, to_csv


if __name__=="__main__":
    print 'import calendar test --> csv files'
    all_courses = ['INFOH500','BIMEH404','STATH400']
    host = 'http://164.15.72.157:8080'
    first_monday = '20/09/2010'

    for course in all_courses:
        dest_filename = 'agenda_%s.csv' % course
        print "Saving %s events to %s" % (course, dest_filename)
        cal = CourseCalendar(host, course)
        cal.load_events()
        csv_string = to_csv(cal.metadata, cal.events, first_monday)
        print csv_string
        export_csv(cal.metadata, cal.events, dest_filename, first_monday)
