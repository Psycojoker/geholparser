'''
Created on Oct 2, 2010
ULB Gehol to CSV calendar converter 
@author: epd
'''
import urllib
from BeautifulSoup import BeautifulSoup 
import re
import csv
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
#    process names ...
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
#    jump to the calendar table    
    cal = tables[1]
    lines = cal.findAll(name='tr',recursive=False)
#    isolate first tab line with hours
    hours_line = lines[0].findAll(name='td',recursive=False)
    hours = []
    for h in hours_line[1:]:
        hours.append(convert_time(h.string))
#    process all lines
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
                # activity
                event['type'] = cell[1].tr.td.contents[0].string
                current_time = current_time + event['duration'] 
                event_list.append(event)
            else:
                current_time = current_time + 1
#    now event are ready for export            
    return event_list

def export_csv(head,events,filename,first_monday):
    '''export events into csv format
    the file is saved under filename (proper .csv extension is added automatically) 
    Google calendar import format:
    Subject,Start Date,Start Time,End Date,End Time,All Day Event,Description,Location,Private
    Final Exam,05/12/08,07:10:00 PM,05/12/08,10:00:00 PM,False,Two essay questions that will cover topics covered throughout the semester,"Columbia, Schermerhorn 614",True
    first_monday corresponds to the monday date of week 1 in Gehol 
    '''
    date_init = datetime.strptime(first_monday,'%d/%m/%Y')
    writer = csv.writer(open('%s.csv'%filename, 'w'), delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #write header line see google help http://www.google.com/support/calendar/bin/answer.py?answer=45656
    writer.writerow(['Subject','Start Date','Start Time','End Date','End Time','All Day Event','Description','Location','Private'])
    for event in events:
        for sub in event['weeks']:
            subject = '%s%s'%(head['mnemo'],event['type'])
            #add offset corresponding to week numbers for each event repetition
            delta = timedelta(days=(sub-1)*7+(event['day']))
            start_date = (date_init+delta).strftime("%d/%m/%y")
            start_time = event['start'].strftime("%I:%M:%S %p")
            end_date = start_date
            end_time = event['end'].strftime("%I:%M:%S %p")
            all_day_event = 'False'
            description = head['title']+' titulaire : '+ head['tutor']
            location = event['location']
            private = 'True'
            writer.writerow([subject,start_date,start_time,end_date,end_time,
                         all_day_event,description,location,private])

def test():
    '''test import function for a mnemonic list'''
    print 'import calendar test'
    mnemo = ['INFOH500','BIMEH404','STATH400']
    host = 'http://164.15.72.157:8080'
    first_monday = '20/09/2010'
    
    for m in mnemo:
        html = get_html(host,m)
        head = parse_header(html)
        print head
        events = parse_table(html)
        export_csv(head, events, 'agenda_%s'%m,first_monday)
    
if __name__ == '__main__':
    '''Import calendar directly from the ULB webserver and convert the calendar
    into a CVS file compatible with google calendar
    this version is used only with the "by course" calendars
    '''
    test()