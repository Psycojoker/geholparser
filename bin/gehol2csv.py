#!/usr/bin/env python

import argparse
from gehol import GeholProxy
from gehol.converters.csvwriter import export_csv

def main():
    '''Import calendar directly from the ULB webserver and convert the calendar
    into a CSV file compatible with google calendar
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
     
         
     
    args = parser.parse_args()
    if args.mnemo is None:
        parser.print_help()
    else:
        dest_filename = 'agenda_%s.csv' % args.mnemo
        try:
            gehol_proxy = GeholProxy(args.server)
            cal =  gehol_proxy.get_course_calendar(args.mnemo)
            print 'Saving %s (%d events) to %s' % (args.mnemo, len(cal.events), dest_filename )
            export_csv(cal.metadata, cal.events, dest_filename, args.d)

        except Exception, inst:
            print 'problem encountered with \n%s\nNothing saved.\n' % args
            print type(inst)     # the exception instance
            print inst.args      # arguments stored in .args
            print inst           # __str__ allows args to printed directly
        else:
            print 'done'


if __name__ == '__main__':
    main()
