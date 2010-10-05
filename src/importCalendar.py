'''
Created on Oct 2, 2010
ULB Gehol to CSV calendar converter 
@author: epd
'''
import argparse
import urllib
from BeautifulSoup import BeautifulSoup
import re
import csv, codecs, cStringIO
from datetime import datetime, timedelta

def get_html(host,mnemo):
    '''get the html page from the web'''
    params = urllib.urlencode({'template': 'cours', 'weeks': '1-31', 'days': '1-6', 'periods':'5-29', 'width':0,'height':0})
    url = '%s/Reporting/Individual;Courses;name;%s?%s'%(host,mnemo,params)
    f = urllib.urlopen(url)
    return f.read()

def split_weeks(weeks):
    '''split string containing weeks info into separated fields
    e.g. "1,5-7"  ---> [1,5,6,7]'''
    s = weeks.split(',')
    w = []
    for f in s:
        sf = f.split('-')
        if len(sf)>1:
            w.extend(range(int(sf[0]),int(sf[1])+1))
        else:
            w.append(int(f))  
    return w

def parse_header(html):
    '''parse html page to find global informations''' 
    soup = BeautifulSoup(html)
    #process names ...
    bTag = soup.find('td',text=re.compile('Horaire'))
    head = {}
    head['mnemo'] = bTag.split(':')[1].split('-')[0].lstrip()
    head['title'] = bTag.split(':')[1].split('-')[1].lstrip()
    bTag = soup.find('td',text=re.compile('Titulaire'))
    head['tutor'] = bTag.split(':')[1].lstrip()
    return head

def convert_time(s):
    '''convert string time into datetime struct'''
    d = datetime.strptime(s,"%H:%M")
    return d

def parse_table(html):
    '''parse html page and process the calendar table
    intermediate python structure (event list) is returned''' 
    soup = BeautifulSoup(html)
    tables = soup.html.body.findAll(name='table',recursive=False)
    #jump to the calendar table    
    cal = tables[1]
    lines = cal.findAll(name='tr',recursive=False)
    #isolate first tab line with hours
    hours_line = lines[0].findAll(name='td',recursive=False)
    hours = []
    for h in hours_line[1:]:
        hours.append(convert_time(h.string))
    #process all lines
    event_list = []
    for (day,line) in enumerate(lines[1:]):
        slots = line.findAll(name='td',recursive=False)
        current_time = -1
        for s in slots:
            cell = s.findAll(name='table',recursive=False)
            # event found
            if len(cell)>1:
                event = {}
                event['day'] = day
                event['start'] = hours[current_time]
                #duration in hours is extract from the colspan 
                event['duration'] = (int(s['colspan']))
                #compute end time (1 colspan=1/2 hour)
                delta = timedelta(hours=event['duration']/2)
                event['end'] = hours[current_time]+delta
                td = cell[0].tr.findAll(name='td',recursive=False)
                # Gehol weeks when the event occurs
                event['weeks'] = split_weeks(td[0].contents[0].string)
                # location
                
                event['location'] = td[1].contents[0].string
                if event['location'] is None:
                    event['location'] = ''
                # activity
                event['type'] = cell[1].tr.td.contents[0].string
                current_time = current_time + event['duration'] 
                event_list.append(event)
            else:
                current_time = current_time + 1
    #now event are ready for export            
    return event_list

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

def export_csv(head,events,filename,first_monday):
    '''export events into csv format
    the file is saved under filename .csv extension must be provided 
    Google calendar import format:
    Subject,Start Date,Start Time,End Date,End Time,All Day Event,Description,Location,Private
    Final Exam,05/12/08,07:10:00 PM,05/12/08,10:00:00 PM,False,Two essay questions that will cover topics covered throughout the semester,"Columbia, Schermerhorn 614",True
    first_monday corresponds to the monday date of week 1 in Gehol 
    '''
    date_init = datetime.strptime(first_monday,'%d/%m/%Y')
    writer = UnicodeWriter(open(filename, 'w'), delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #write header line see google help http://www.google.com/support/calendar/bin/answer.py?answer=45656
    writer.writerow(['Subject','Start Date','Start Time','End Date','End Time','All Day Event','Description','Location','Private'])
    for event in events:
        n = len(event['weeks'])
        for (i,sub) in enumerate(event['weeks']):
            subject = '%s%s (%d/%d)'%(head['mnemo'],event['type'],i+1,n)
            #add offset corresponding to week numbers for each event repetition
            delta = timedelta(days=(sub-1)*7+(event['day']))
            start_date = (date_init+delta).strftime("%d/%m/%y")
            start_time = event['start'].strftime("%I:%M:%S %p")
            end_date = start_date
            end_time = event['end'].strftime("%I:%M:%S %p")
            all_day_event = 'False'
            description = head['title']+' titulaire : '+ head['tutor']
            location = event['location']
            private = 'False'
            writer.writerow([subject,start_date,start_time,end_date,end_time,
                         all_day_event,description,location,private])

def test():
    '''test import function for a mnemonic list'''
    print 'import calendar test --> csv files'
    mnemo = ['INFOH500','BIMEH404','STATH400']
    host = 'http://164.15.72.157:8080'
    first_monday = '20/09/2010'
    
    for m in mnemo:
        dest_filename = 'agenda_%s.csv'%m
        process(m, host, first_monday, dest_filename)
        print dest_filename

def process(mnemo,host,first_monday,dest_filename):    
    html = get_html(host,mnemo)    
    head = parse_header(html)
    events = parse_table(html)
    export_csv(head, events, dest_filename,first_monday)
    
if __name__ == '__main__':
    '''Import calendar directly from the ULB webserver and convert the calendar
    into a CVS file compatible with google calendar
    this version is used only with the "by course" calendars
    '''
    parser = argparse.ArgumentParser(description='Fetch Gehol calendar from the ULB web page and generate a csv file compatible with google calendar.',
                                     epilog="THIS PROGRAM IS GIVEN AS THIS WITHOUT ANY GARANTEE")
    #positional argument
    parser.add_argument('mnemo', nargs='?', default=None)
    #optional arguments
    parser.add_argument('-s','--server', required=False, help='server address [http://164.15.72.157:8080]',default = 'http://164.15.72.157:8080')
    parser.add_argument('-d', required=False, help='Monday date of the week 1 [20/09/2010]',default = '20/09/2010')
    parser.add_argument('-t','--test', required=False, action='store_true',help='test the program on some courses',default = False)
    
    args = parser.parse_args()
    if args.test:
        test()
    else:
        if args.mnemo is None:
            parser.print_help()
        else:
            dest_filename = 'agenda_%s.csv'%args.mnemo
            try:
                process(args.mnemo, args.server, args.d, dest_filename)
            except:
                print 'problem encountered with \n%s\nNothing saved.'%args
            else:
                print '%s saved'%dest_filename            