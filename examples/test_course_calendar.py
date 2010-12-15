import sys
sys.path.append('../src')

from gehol.coursecalendar import CourseCalendar


if __name__=="__main__":
    from pprint import pprint
    calendar = CourseCalendar("164.15.72.157:8080", "INFOH500")
    print "getting events from : %s" % calendar.url
    calendar.load_events()
    pprint(calendar.events)
    print len(calendar.events)
    print calendar.metadata
