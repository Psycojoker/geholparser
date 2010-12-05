import sys
sys.path.append("../src")

from coursecalendar import CourseCalendar
from csvwriter import export_csv


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
        export_csv(cal.metadata, cal.events, dest_filename, first_monday)


