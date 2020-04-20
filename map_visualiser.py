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
import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, cm


#############################################################
#
# Help function
#
#############################################################

def showHelp(logger):

    logger.info("  This script plots the area of a NetCDF file.")
    logger.info("  Parameters are:")
    logger.info("  --inputFile=<FILE>")
    logger.info("  --function=<boundaries|winds|currents|temperature>")
    logger.info("  --latVariable=<LATVAR>")
    logger.info("  --lonVariable=<LONVAR>")
    logger.info("  --plotVariable=<PLOTVAR>")
    

#############################################################
#
# Get Boundaries
#
#############################################################

def getBoundaries(ds):
    
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

    # return
    return latMin, latMax, lonMin, lonMax


#############################################################
#
# Plot Boundaries
#
#############################################################

def plotBoundaries(ds, inputFile):

    # get boundaries
    latMin, latMax, lonMin, lonMax = getBoundaries(ds)
    
    # plot them
    m = Basemap(projection='merc',
                llcrnrlat=latMin, urcrnrlat=latMax,
                llcrnrlon=lonMin, urcrnrlon=lonMax,                    
                resolution='l')

    # add coastlines, states, and country boundaries
    m.drawcoastlines()
    m.drawstates()
    m.drawcountries()

    # add color
    m.fillcontinents(color='coral',lake_color='aqua')

    # set the title
    plt.title(inputFile)
            
    # show the plot
    plt.show()
    
    
#############################################################
#
# Plot Winds
#
#############################################################

def plotWinds(ds, inputFile, windVar):

    # get boundaries
    latMin, latMax, lonMin, lonMax = getBoundaries(ds)
    
    # plot them
    m = Basemap(projection='merc',
                llcrnrlat=latMin, urcrnrlat=latMax,
                llcrnrlon=lonMin, urcrnrlon=lonMax,                    
                resolution='l')

    # Add Coastlines, States, and Country Boundaries
    m.drawcoastlines()
    m.drawstates()
    m.drawcountries()

    # add color
    m.fillcontinents(color='coral',lake_color='aqua')

    # set the title
    plt.title(inputFile)

    # get data for winds
    lons = ds.variables[lonVar][:]
    lats = ds.variables[latVar][:]
    tmax = ds.variables[windVar][0,:,:]
    lon, lat = np.meshgrid(lons, lats)
    xi, yi = m(lon, lat)
    cs = m.pcolor(xi, yi, np.squeeze(tmax))
    
    # show the plot
    plt.show()


#############################################################
#
# Plot Temperature
#
#############################################################

def plotTemperature(ds, inputFile, tempVar):
    logger.error("Not yet implemented")

    
#############################################################
#
# Plot Currents
#
#############################################################

def plotCurrents(ds, inputFile, currentsVar):
    logger.error("Not yet implemented")
    

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
    function = None
    try:
        options, rem = getopt.getopt(sys.argv[1:], 'i:hf:p:', ['inputFile=', 'help', 'latVariable=', 'lonVariable=', 'function=', 'plotVariable='])
    
        for opt, arg in options:
            if opt in ('-i', '--inputFile'):
                inputFile = arg
            elif opt in ('--latVariable'):                
                latVar = arg
            elif opt in ('--lonVariable'):                
                lonVar = arg
            elif opt in ('-f', '--function'):
                function = arg
            elif opt in ('-p', '--plotVariable'):
                plotVar = arg
            elif opt in ('-h', '--help'):
                showHelp(logger)
                sys.exit(0)
    
    except getopt.GetoptError:
        showHelp(logger)
        sys.exit(1)

    if (not function) or (not inputFile):
        logger.error("wrong number of arguments!")
        showHelp(logger)
        sys.exit(1)    

        
    #############################################################
    #
    # Invoke the right function
    #
    #############################################################

    # open netCDF file
    ds = Dataset(inputFile, "r")

    # invoke the proper function
    if function == "boundaries":
        plotBoundaries(ds, inputFile)
    elif function == "winds":
        plotWinds(ds, inputFile, plotVar)
    elif function == "currents":
        plotCurrents(ds, inputFile, plotVar)
    elif function == "temperature":
        plotTemperature(ds, inputFile, plotVar)
    
    # close file
    ds.close()
