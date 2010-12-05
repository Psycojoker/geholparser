#!/usr/bin/env python

import argparse

from importCalendar import get_html, get_html_by_url, parse_header, parse_table
from csvwriter import export_csv

def process(mnemo,host,first_monday,dest_filename):    
    html = get_html(host,mnemo)    
    head = parse_header(html)
    events = parse_table(html)
    export_csv(head, events, dest_filename,first_monday)

    
def process_by_url(url,first_monday,dest_filename):    
    html = get_html_by_url(url)    
    head = parse_header(html)
    events = parse_table(html)
    export_csv(head, events, dest_filename,first_monday)


def test_all():
    test_batch()
    test_with_url()


def test_batch():
    '''test import function for a mnemonic list'''
    print 'import calendar test --> csv files'
    mnemo = ['INFOH500','BIMEH404','STATH400']
    host = 'http://164.15.72.157:8080'
    first_monday = '20/09/2010'
    
    for m in mnemo:
        dest_filename = 'agenda_%s.csv' % m
        process(m, host, first_monday, dest_filename)
        print dest_filename


def test_with_url():
    #test by url
    first_monday = '20/09/2010'
    url = 'http://164.15.72.157:8080/Reporting/Individual;Student%20Set%20Groups;id;%23SPLUSA629A0?&template=Ann%E9e%20d%27%E9tude&weeks=1-14&days=1-6&periods=5-33&width=0&height=0'
    dest_filename = 'import_by_url.csv'
    process_by_url(url, first_monday, dest_filename)



    
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
    parser.add_argument('-s','--server', required=False,
                        help='server address [http://164.15.72.157:8080]',
                        default = 'http://164.15.72.157:8080')

    parser.add_argument('-d', required=False,
                        help='Monday date in the week 1 [20/09/2010]',
                        default = '20/09/2010')


    parser.add_argument('-t','--test', required=False,
                        action='store_true',
                        help='test the program on some courses',
                        default = False)


    parser.add_argument('-b','--test_batch', required=False,
                        action='store_true',
                        help='test the program on a batch of courses',
                        default = False)

    parser.add_argument('-u','--test_url', required=False,
                        action='store_true',
                        help='test the program on a course by supplying a full url',
                        default = False)



    args = parser.parse_args()
    if args.test:
        test_all()
    elif args.test_batch:
        test_batch()
    elif args.test_url:
        test_with_url()
    else:
        if args.mnemo is None:
            parser.print_help()
        else:
            dest_filename = 'agenda_%s.csv' % args.mnemo
            try:
                process(args.mnemo, args.server, args.d, dest_filename)
            except Exception, inst:
                print 'problem encountered with \n%s\nNothing saved.\n' % args
                print type(inst)     # the exception instance
                print inst.args      # arguments stored in .args
                print inst           # __str__ allows args to printed directly                
            else:
                print '%s saved\n' % dest_filename            
