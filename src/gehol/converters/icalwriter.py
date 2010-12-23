from datetime import datetime, timedelta
from icalendar import Calendar, Event, vText



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

    #        cal_event.add('dtend', datetime(2005,4,4,10,0,0,tzinfo=UTC))
    #        cal_event.add('dtstamp', datetime(2005,4,4,0,10,0,tzinfo=UTC))
    #        event['uid'] = '20050115T101010/27346262376@mxm.dk'
    #        event.add('priority', 5)

            cal.add_component(cal_event)

    return cal.as_string()



def convert_student_calendar_to_ical(student_calendar, first_monday):
    date_init = datetime.strptime(first_monday,'%d/%m/%Y')

    ical = Calendar()
    ical.add('prodid', 'https://bitbucket.org/odebeir/geholimport')
    ical.add('version', '2.0')
    ical.add('summary', student_calendar.description)
    ical.add('x-wr-calname', student_calendar.profile)
    ical.add('x-wr-caldesc', student_calendar.description)

    print "adding : %d events" % len(student_calendar.events)


    for event in student_calendar.events:
        # get some common data for all generated events
        event_summary =  "%s (%s)" % (event['title'], event['type'])
        event_organizer = event['organizer']
        event_location = event['location']
        #print 'expanding events for %s' % event_summary.encode('iso-8859-2')

        #expand to ical events
        for (i, event_week) in enumerate(event['weeks']):
            delta = timedelta(days=(event_week-1)*7+(event['day']))
            dtstart = date_init+delta + timedelta(hours = event['start_time'].hour,
                                                    minutes = event['start_time'].minute)
            dtend = date_init+delta + timedelta(hours = event['stop_time'].hour,
                                            minutes = event['stop_time'].minute)
            ical_event = Event()

            ical_event.add('summary', event_summary)
            ical_event.add('location', event_location)
            ical_event.add('cn', "foo")#event_organizer.encode('iso-8859-2'))
            ical_event.add('dtstart', dtstart)
            ical_event.add('dtend', dtend)

            ical.add_component(ical_event)

    return ical.as_string()



def export_ical(head,events,dest_filename, first_monday):
    ical_string = to_ical(head,events,first_monday)
    fd = open(dest_filename,'w')
    fd.write(ical_string)


def write_ical_to_file(ical_data, dest_filename):
    fd = open(dest_filename,'w')
    fd.write(ical_data)