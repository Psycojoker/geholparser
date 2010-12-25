import sys
sys.path.append('../src')

from gehol import GeholProxy


def test_valid_course(course_mnemo="INFOH500"):
    gehol_proxy = GeholProxy("164.15.72.157:8080")
    print "Fetching events for course : %s" % course_mnemo
    calendar = gehol_proxy.get_course_calendar(course_mnemo)
    print "Result : "
    print calendar


def test_nonexistent_course():
    course_mnemo = "INFOH999"
    print "Fetching events for non existent course : %s" % course_mnemo
    gehol_proxy = GeholProxy("164.15.72.157:8080")
    try:
        calendar = gehol_proxy.get_course_calendar(course_mnemo)
    except Exception,e:
        print "Non existent course %s was not found" % course_mnemo
        print "Reason : ", e.message


if __name__=="__main__":
    test_valid_course()
    print "-----"
    test_nonexistent_course()
