__author__ = 'bouska'

from datetime import datetime, timedelta
from StringIO import StringIO


class Event(object):
    def __init__(self):
        self.summary = ""
        self.organizer = ""
        self.location = ""
        self.description = ""
        self.start = None
        self.duration = None


class Calendar(object):
    def __init__(self):
        self.name = ""
        self.description = ""
        self.version = "2.0"
        self.provider = "https://bitbucket.org/odebeir/geholimport"
        self.start_date = datetime.today()
        self.events = []


    def add_event(self, event):
        self.events.append(event)


    def as_string(self):
        def write_line(out, line):
            out.write(line+'\n')

        out = StringIO()

        def dirty_fix(duration):
            def total_seconds(td):
                return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6
            seconds = total_seconds(duration)
            hours = seconds / 60 / 60
            minutes = seconds / 60 % 60
            return "%02i:%02i" % (hours, minutes)

        for event in self.events:
            write_line(out, "REM %s AT %s DURATION %s MSG %s (%s)" %
                       (str(event.start.strftime("%b %d %Y")),
                        str(event.start.strftime("%H:%M")),
                       str(dirty_fix(event.duration)),
                       str(event.summary),
                       str(event.location)))

        ical_string = out.getvalue()
        out.close()

        return ical_string.encode('utf-8')



def convert_geholcalendar_to_remind(gehol_calendar, first_monday):
    date_init = datetime.strptime(first_monday,'%d/%m/%Y')

    cal = Calendar()
    cal.description = gehol_calendar.description
    cal.name = gehol_calendar.name
    cal.start_date = date_init

    for event in gehol_calendar.events:
        remind_event = Event()

        for (i, event_week) in enumerate(event.weeks):
            delta = timedelta(days=(event_week-1)*7 + event.day)
            start = date_init+delta + timedelta(hours = event.start_time.hour,
                                                  minutes = event.start_time.minute)
            duration = timedelta(hours = event.stop_time.hour,
                                  minutes = event.stop_time.minute) -  timedelta(hours = event.start_time.hour,
                                                  minutes = event.start_time.minute) 

            remind_event = Event()
            remind_event.summary = event.summary
            remind_event.location = event.location
            #remind_event.description = event.description
            #remind_event.organizer = event.organizer

            remind_event.start = start
            remind_event.duration = duration

            cal.add_event(remind_event)

    return cal
