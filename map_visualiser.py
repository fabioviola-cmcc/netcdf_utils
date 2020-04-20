#!/usr/bin/python3

#############################################################
#
# requirements
#
#############################################################

import pdb
import sys
import getopt
import logging
from netCDF4 import Dataset
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, cm


#############################################################
#
# Help function
#
#############################################################

def showHelp(logger):

    logger.info("This script plots the area of a NetCDF file.")
    logger.info("Invoke this script with --inputFile=<FILE> --latVariable=<LATVAR> --lonVariable=<LONVAR>")


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
    logger = logging.getLogger('map_visualiser')
    logger.setLevel(logging.DEBUG)
    logging.getLogger("matplotlib").setLevel(logging.CRITICAL)
    
    
    #############################################################
    #
    # Process command-line arguments
    #
    #############################################################

    inputFile = None
    try:
        options, rem = getopt.getopt(sys.argv[1:], 'i:h', ['inputFile=', 'help', 'latVariable=', 'lonVariable='])
    
        for opt, arg in options:
            if opt in ('-i', '--inputFile'):
                inputFile = arg
            elif opt in ('--latVariable'):                
                latVar = arg
            elif opt in ('--lonVariable'):                
                lonVar = arg                                
            elif opt in ('-h', '--help'):
                showHelp(logger)
                sys.exit(0)
    
    except getopt.GetoptError:
        showHelp(logger)
        sys.exit(1)

    if not inputFile:
        logger.error("wrong number of arguments!")
        showHelp(logger)
        sys.exit(1)    

        
    #############################################################
    #
    # Process files
    #
    #############################################################

    # open netCDF file
    ds = Dataset(inputFile, "r")

    # get coordinates
    try:
        latMin = ds.variables[latVar][:].data.min()
        latMax = ds.variables[latVar][:].data.max()
        lonMin = ds.variables[lonVar][:].data.min()
        lonMax = ds.variables[lonVar][:].data.max()
    except KeyError:
        logger.error("Check your variables!")
        sys.exit(1)
        
    logger.debug("Latitude bounds are %s and %s" % (latMin, latMax))
    logger.debug("Longitude bounds are %s and %s" % (lonMin, lonMax))
    
    # - plot them
    m = Basemap(projection='merc',
                llcrnrlat=latMin,
                urcrnrlat=latMax,
                llcrnrlon=lonMin,
                urcrnrlon=lonMax,                    
                resolution='l')
    m.drawcoastlines()
    m.fillcontinents(color='coral',lake_color='aqua')
    plt.title(inputFile)
    plt.show()
        
    # close file
    ds.close()
