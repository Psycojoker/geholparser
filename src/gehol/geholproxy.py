
import urllib
import httplib
from coursecalendar import CourseCalendar


class GeholProxy(object):
    """
    Entry point for all Gehol queries
    """
    def __init__(self, host="http://164.15.72.157:8080"):
        """
        - host: optionnal gehol host string. Default value = "http://164.15.72.157:8080"
        """
        self.host = host


    def get_course_calendar(self, course_mnemonic):
        """
        Performs a Gehol query and retrieves the events associated to the given course

        - course_mnemonic: string
        """
        url = self._build_course_query_url(course_mnemonic)
        html_data = self._get_html_data(url)
        cal = CourseCalendar(html_data)
        return cal


    def _build_course_query_url(self, mnemo):
        """
        Builds a Gehol query url for the given course mnemonic.
        """
        params = urllib.urlencode({'template': 'cours',
                                   'weeks': '1-31',
                                   'days': '1-6',
                                   'periods':'5-29',
                                   'width':0,
                                   'height':0})
        url = '%s/Reporting/Individual;Courses;name;%s?%s'%(self.host, mnemo, params)
        return url


    def _get_html_data(self, url):
        """
        Fetches html data. Returns a file-like object from which to read the data from.
        """
        try:
            html_page = urllib.urlopen(url)
            return html_page
        except:
            raise ValueError('Could not get fetch url : %s' % url)