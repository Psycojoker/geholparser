import sys
sys.path.append('../src')

from CourseCalendar import CourseCalendar


if __name__=="__main__":
    from pprint import pprint
    calendar = CourseCalendar("http://164.15.72.157:8080", "INFOH500")
    print "getting events from : %s" % calendar.url
    calendar.load_events()
    pprint(calendar.events)
    print len(calendar.events)
