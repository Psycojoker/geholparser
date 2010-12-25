__author__ = 'sevas'


class GeholException(Exception):
    pass

class CourseNotFoundException(GeholException):
    pass

class UnknowErrorException(GeholException):
    pass
