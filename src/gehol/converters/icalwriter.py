from datetime import datetime, timedelta
from icalendar import Calendar, Event, vText
from StringIO import StringIO



def to_ical(head,events,first_monday):
    '''export events into iCal format
    the file is returned as a string
    first_monday corresponds to the monday date of week 1 in Gehol
    '''
    date_init = datetime.strptime(first_monday,'%d/%m/%Y')

    cal = Calendar()
    cal.add('prodid', 'https://bitbucket.org/odebeir/geholimport')
    cal.add('version', '2.0')
    cal.add('summary', head['title'])
    cal.add('x-wr-calname', "%s - %s"  % (head['mnemo'], head['title']))
    cal.add('x-wr-caldesc', "%s - %s (%s)" % (head['mnemo'], head['title'], head['tutor']))

    for event in events:
        n = len(event['weeks'])
        for (i,sub) in enumerate(event['weeks']):
            summary = '%s%s (%d/%d)'%(head['mnemo'],event['type'],i+1,n)
            #add offset corresponding to week numbers for each event repetition
            delta = timedelta(days=(sub-1)*7+(event['day']))
            dtstart = date_init+delta + timedelta(hours = event['start'].hour,
                                                  minutes = event['start'].minute)
            dtend = date_init+delta + timedelta(hours = event['end'].hour,
                                                minutes = event['end'].minute)

            organizer = head['title']+' titulaire : '+ head['tutor']
            location = event['location']

            cal_event = Event()

            cal_event.add('summary', summary)
            cal_event.add('dtstart', dtstart)
            cal_event.add('dtend', dtend)
            cal_event['location'] = vText(location)
            cal_event['organizer'] = vText(organizer)

            cal.add_component(cal_event)

    return cal.as_string()


def convert_calendar_to_ics_rfc5545(calendar, first_monday):
    date_init = datetime.strptime(first_monday,'%d/%m/%Y')

    def write_line(out, line):
        out.write(line+'\r\n')

    out = StringIO()
    write_line(out, "BEGIN:VCALENDAR")
    write_line(out, "VERSION:%s" % "2.0")
    write_line(out, "PRODID:%s" % 'https://bitbucket.org/odebeir/geholimport')

    write_line(out, "X-WR-CALNAME:%s" % calendar.name)
    write_line(out, "X-WR-CALDESC:%s" % calendar.description)

    write_line(out, "BEGIN:VTIMEZONE")
    write_line(out, "TZID:Europe/Brussels")
    write_line(out, "BEGIN:STANDARD")
    write_line(out, "TZOFFSETFROM:+0100")
    write_line(out, "TZOFFSETTO:+0100")
    write_line(out, "DTSTART:%s" % date_init.strftime("%Y%m%dT%H%M%S"))
    write_line(out, "END:STANDARD")
    write_line(out, "END:VTIMEZONE")


    for event in calendar.events:
        event_summary =  "%s (%s)" % (event['title'], event['type'])
        event_organizer = event['organizer']
        event_location = event['location']
        event_description = "%s [%s]" % (event_summary, event_organizer)

        for (i, event_week) in enumerate(event['weeks']):
            delta = timedelta(days=(event_week-1)*7+(event['day']))
            dtstart = date_init+delta + timedelta(hours = event['start_time'].hour,
                                                    minutes = event['start_time'].minute)
            dtend = date_init+delta + timedelta(hours = event['stop_time'].hour,
                                            minutes = event['stop_time'].minute)

            write_line(out, "BEGIN:VEVENT")
            write_line(out, "DTSTAMP:%s" %  dtstart.strftime("%Y%m%dT%H%M%S"))
            write_line(out, "DTSTART;TZID=Europe/Brussels:%s" % dtstart.strftime("%Y%m%dT%H%M%S"))
            write_line(out, "DTEND;TZID=Europe/Brussels:%s" % dtend.strftime("%Y%m%dT%H%M%S"))
            write_line(out, "SUMMARY:%s" % event_summary)
            write_line(out, "DESCRIPTION:%s" % event_description)
            write_line(out, "LOCATION:%s" % event_location)
            #write_line(out, "GEO:5.092867;51.557655")
            write_line(out, "END:VEVENT")

    write_line(out, "END:VCALENDAR")
    ical_string = out.getvalue()
    out.close()

    return ical_string.encode('utf-8')


def export_ical(head,events,dest_filename, first_monday):
    ical_string = to_ical(head,events,first_monday)
    fd = open(dest_filename,'w')
    fd.write(ical_string)


def write_ical_to_file(ical_data, dest_filename):
    fd = open(dest_filename,'w')
    fd.write(ical_data)