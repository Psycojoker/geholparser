
import urllib
import urlparse
import httplib
from coursecalendar import CourseCalendar, GeholException


class GeholProxy(object):
    """
    Entry point for all Gehol queries
    """
    def __init__(self, host="164.15.72.157:8080"):
        """
        - host: optionnal gehol host string. Default value = "164.15.72.157:8080"
        """
        self.host = host

    def get_course_calendar(self, course_mnemonic):
        """
        Builds a Gehol query YRL and retrieves the events associated to the given course

        - course_mnemonic: string
        """
        url = self._build_course_query_url(course_mnemonic)
        return self.get_course_calendar_from_url("http://%s%s" %  (self.host,url))
        

    def get_course_calendar_from_url(self, url):
        """
        Performs a Gehol query and retrieves the events associated to the given course

        - url: valid Gehol URL
        """
        parsed_url = urlparse.urlparse(url)
        scheme, netloc, path, params, query, frag = parsed_url
        self.host = netloc
        html_data = self._get_html_data("%s;%s?%s" % (path, params, query))
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
        url = '/Reporting/Individual;Courses;name;%s?%s'%(mnemo, params)
        return url


    def _get_html_data(self, url):
        """
        Fetches html data. Returns a file-like object from which to read the actual content.
        """
        try:
            headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
            conn = httplib.HTTPConnection(self.host)
            conn.request("GET", url, headers = headers)
            response = conn.getresponse()        
            return response
        except GeholException,e:
            raise ValueError('Could not get fetch url : %s (Reason : %s)' % (url, e.message))
        
