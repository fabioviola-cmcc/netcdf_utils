#!/usr/bin/python3

# reqs
import sys
from datetime import datetime, timedelta

# read input
d = float(sys.argv[1])
int_part = int(d)
dec_part = float(d)-int(d)

# produce and print result
converted = datetime.fromordinal(int_part) + timedelta(dec_part%1)
print(converted.strftime("%A, %d. %B %Y %I:%M%p"))
