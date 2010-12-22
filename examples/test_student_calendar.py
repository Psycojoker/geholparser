#!/usR/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Frederic'

import sys
sys.path.append("../src")
from gehol.studentcalendar import StudentCalendar
from pprint import pprint

DATA_FILE = "../data/student/IR_MA1_img_1_31.html"

if __name__ == "__main__":
    f = open(DATA_FILE)
    cal = StudentCalendar(f)
    print cal.header_data
    pprint(cal.events)

    #fuuuu = cal.events['monday'][0]['type'].encode('utf-8')



