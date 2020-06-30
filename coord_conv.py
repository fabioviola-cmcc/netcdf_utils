#!/usr/bin/python3

# reqs
import sys

# read command line arguments
lat = float(sys.argv[1])
lon = float(sys.argv[2])

# debug print
print("\n=== INPUT DATA ===")
print(" - Latitude: %s" % lat)
print(" - Longitude: %s" % lon)

# convert latitude
lat_deg = int(lat)
dec_part = lat - int(lat)
lat_min = round(dec_part * 60, 2)
print("\n=== OUTPUT DATA ===")
print(" - Output latitude: %s deg %s min" %(lat_deg, lat_min))

# convert longitude
lon_deg = int(lon)
dec_part = lon - int(lon)
lon_min = round(dec_part * 60, 2)
print(" - Output longitude: %s deg %s min\n" %(lon_deg, lon_min))
