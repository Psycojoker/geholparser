import sys
sys.path.append('../src')

from gehol import GeholProxy

def test_course_url(url):
    gehol_proxy = GeholProxy()
    calendar = gehol_proxy.get_course_calendar_from_url(url)
    print "Result : %s" % calendar

if __name__ == '__main__':
    URL = "http://164.15.72.157:8080/Reporting/Individual;Courses;name;INFOH500?&template=Cours&weeks=1-14&days=1-6&periods=5-29&width=0&height=0"
    test_course_url(URL)
