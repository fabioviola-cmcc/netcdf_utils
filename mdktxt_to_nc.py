#!/bin/python3
#
# This script converts .rel files produced by Medslik-II to
# netCDF4 file containing environmental variables.
# The output netCDF4 file includes the same dimensions as the
# wind files used by Medslik-II as input (lat, lon, time) as
# well as the same variables (lat, lon, time, U10M and V10M).
#
# written by: Fabio Viola (2020/04/21)
#


#############################################################
#
# requirements
#
#############################################################

# global reqs
import csv
import pdb
import sys
import math
import getopt
import logging
import subprocess
import numpy as np
from netCDF4 import Dataset
from netCDF4 import date2num
from datetime import datetime


#############################################################
#
# printHelp
#
#############################################################

def printHelp(logger):
    logger.error("Not yet implemented!")


#############################################################
#
# Main
#
#############################################################

if __name__ == "__main__":

    #############################################################
    #
    # Configure logger
    #
    #############################################################

    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('mdk2nc')
    logger.setLevel(logging.DEBUG)
    
    
    #############################################################
    #
    # Process command-line arguments
    #
    #############################################################

    inputFile = outputFile = timeStep = None
    
    try:
        options, rem = getopt.getopt(sys.argv[1:], 'i:o:ht:', ['inputFile=', 'outputFile=','help', "time="])
    
        for opt, arg in options:
            if opt in ('-i', '--inputFile'):
                inputFile = arg
                csvFile = inputFile + ".csv"
                outputFile = inputFile + ".nc"
            elif opt in ('-o', '--outputFile'):
                outputFile = arg
            elif opt in ('-t', '--time'):
                timeStep = arg
            elif opt in ('-h', '--help'):
                printHelp(logger)
                sys.exit(0)
    
    except getopt.GetoptError:
        logger.error("wrong arguments!")
        printHelp(logger)
        sys.exit(1)

    if (not inputFile) and (not timeStep):
        logger.error("wrong number of arguments!")
        printHelp(logger)
        sys.exit(1)    
    
        
    #############################################################
    #
    # Start processing
    #
    #############################################################

    logger.debug("Starting processing")

    # open the output netCDF4 file
    logger.debug("Initialising output netCDF4 file")
    ds = Dataset(outputFile, "w")

    # TODO
    logger.debug("Setting attributes")

    # create dimensions lat, lon, time
    logger.debug("Creating dimensions")
    ds.createDimension("lat")
    ds.createDimension("lon")
    ds.createDimension("time")

    # create variables
    logger.debug("Creating variables")
    lat_var = ds.createVariable("lat", np.float32, ("lat",))
    lon_var = ds.createVariable("lon", np.float32, ("lon",))
    time_var = ds.createVariable("time", np.int32, ("time",))
    u10m_var = ds.createVariable("U10M", np.float32, ("time", "lat", "lon",))
    v10m_var = ds.createVariable("V10M", np.float32, ("time", "lat", "lon",))

    # start filling variables...
    logger.debug("Filling variables")

    # 1. initialize empty numpy arays
    # NOTE: we use set to get rid of repetitions
    lat_set = set()
    lon_set = set()

    # 1.1 convert rel to csv file
    bash_command = "cat %s | tr -s \" \" | tr \" \" \",\" | grep -v \"[a-z]\" | tail -n +2 | sed s/^,// > %s" % (inputFile, csvFile)
    subprocess.run(bash_command, shell=True)

    # 2. open csv file
    csv_fd = open(csvFile)
    csv_reader = csv.reader(csv_fd, delimiter=",")

    # 3. set the timestep
    print(timeStep)
    td = datetime.fromisoformat(timeStep)
    dd = date2num(td, "hours since 1950-01-01 00:00")
    time_var[:] = [dd]

    # 4. read and copy latitude and longitude of every line
    #    but also take the value of U10M and V10M
    u10_values = {}
    v10_values = {}
    for row in csv_reader:
        lat_set.add(row[0])
        lon_set.add(row[1])

        # fill u10_values data structure
        if not (row[0] in u10_values.keys()):
            u10_values[row[0]] = {}
        if not (row[1] in u10_values[row[0]].keys()):
            u10_values[row[0]][row[1]] = row[5]
            
        # fill v10_values data structure
        if not (row[0] in v10_values.keys()):
            v10_values[row[0]] = {}
        if not (row[1] in v10_values[row[0]].keys()):
            v10_values[row[0]][row[1]] = row[6]
            
    lat_list = sorted(lat_set)[:]
    lon_list = sorted(lon_set)[:]
    lat_var[:] = lat_list
    lon_var[:] = lon_list
    
    # 5. read and copy U10M and V10M variables        
    u_np_lat = []
    v_np_lat = []
    
    for curr_lat in lat_list:
        
        u_np_lon = []
        v_np_lon = []
        
        for curr_lon in lon_list:

            try:
                u_np_lon.append(u10_values[curr_lat][curr_lon])
                v_np_lon.append(v10_values[curr_lat][curr_lon])
                
            except KeyError:
                u_np_lon.append(float("nan"))
                v_np_lon.append(float("nan"))
                
        u_np_lat.append(np.array(u_np_lon))
        v_np_lat.append(np.array(v_np_lon))
        
    u_np_lat = np.array(u_np_lat)
    v_np_lat = np.array(v_np_lat)

    # push data into netCDF variables U10M and V10M
    u10m_var[0,:,:] = u_np_lat[:,:]
    v10m_var[0,:,:] = v_np_lat[:,:]
    
    # Bye!
    logger.debug("Processing completed")
    ds.close()
