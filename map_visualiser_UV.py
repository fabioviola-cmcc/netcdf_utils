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
import warnings

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
# Get Info
#
#############################################################

def getInfo(ds):

    #pdb.set_trace()
    for v in ds.variables:
        print(v)


def getRangeIndexes(arr, var_min, var_max):
    return np.where((arr >= var_min) & (arr <= var_max))[0]


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
    try:
        lons = ds.variables[lonVar][:]
        lats = ds.variables[latVar][:]
        tmax = ds.variables[windVar][0,:,:]
    except KeyError:
        logger.error("Check your variables!")
        sys.exit(1)        
    lon, lat = np.meshgrid(lons, lats)
    xi, yi = m(lon, lat)
    cs = m.pcolor(xi, yi, np.squeeze(tmax))
    
    # show the plot
    plt.show()


#############################################################
#
# Plot Currents
#
#############################################################

def plotCurrents(dsU, dsV, uVar, vVar):

    # get boundaries
    latMin, latMax, lonMin, lonMax = getBoundaries(dsU)

    for t in range(24):
    
        # create a new figure
        plt.figure()
    
        # get data for currents
        try:
            lons = dsU.variables[lonVar][:]
            lats = dsU.variables[latVar][:]
            umax = dsU.variables[uVar][t,0,:,:]
            vmax = dsV.variables[vVar][t,0,:,:]
            print("Reading variables: ok")
        except KeyError:
            logger.error("Check your variables!")
            sys.exit(1)        
            
        # plot them
        m = Basemap(llcrnrlat=lats.min(), urcrnrlat=lats.max(),
                    llcrnrlon=lons.min(), urcrnrlon=lons.max(),                    
                    resolution='l')
    
        lat_indexes = getRangeIndexes(lats, lats.min(), lats.max())
        lon_indexes = getRangeIndexes(lons, lons.min(), lons.max())
        
        lats_sel = lats[lat_indexes]
        lons_sel = lons[lon_indexes]
        xx, yy = np.meshgrid(lons_sel, lats_sel)
        
        # Add Coastlines, States, and Country Boundaries
        m.drawcoastlines()
        m.drawstates()
        m.drawcountries()
    
        # add color
        m.fillcontinents(color='coral',lake_color='aqua')
    
        # set the title
        plt.title("Currents")
    
        # color the sea
        lon, lat = np.meshgrid(lons, lats)
        xi, yi = m(lon, lat)
        cs = m.pcolor(xi, yi, np.squeeze(umax))
    
        ## draw meridians and parallels
        step_lat = float((latMax - latMin) / 5)
        step_lon = float((lonMax - lonMin) / 5)
    
        # draw arrows
        X = lons[::5]
        Y = lats[::5]
        UU = umax[::5,::5]
        VV = vmax[::5,::5]
        m.quiver(X, Y, UU, VV, scale=3)
    
        # show the plot
        plt.show()
            

#############################################################
#
# Main
#
#############################################################

if __name__ == "__main__":

    # disable warnings
    warnings.filterwarnings("ignore")

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

    inputFiles = None
    function = None
    try:
        options, rem = getopt.getopt(sys.argv[1:], 'i:hf:p:', ['inputFiles=', 'help', 'latVariable=', 'lonVariable=', 'function=', 'plotVariables='])
    
        for opt, arg in options:
            if opt in ('-i', '--inputFiles'):
                inputFiles = arg.split(",")
                print(inputFiles)
            elif opt in ('--latVariable'):                
                latVar = arg
            elif opt in ('--lonVariable'):                
                lonVar = arg
            elif opt in ('-f', '--function'):
                function = arg
            elif opt in ('-p', '--plotVariables'):
                plotVar1, plotVar2 = arg.split(",")
            elif opt in ('-h', '--help'):
                showHelp(logger)
                sys.exit(0)
    
    except getopt.GetoptError:
        showHelp(logger)
        sys.exit(1)

    if (not function) or (not inputFiles):
        logger.error("wrong number of arguments!")
        showHelp(logger)
        sys.exit(1)    

        
    #############################################################
    #
    # Invoke the right function
    #
    #############################################################

    # open netCDF file
    dsU = Dataset(inputFiles[0], "r")
    dsV = Dataset(inputFiles[1], "r")

    # invoke the proper function
    if function == "boundaries":
        plotBoundaries(ds, inputFile)
    elif function == "winds":
        plotWinds(dsU, dsV, inputFile, plotVar1, plotVar2)
    elif function == "currents":
        print("CURRENTS")
        plotCurrents(dsU, dsV, plotVar1, plotVar2)

        # close files
        dsU.close()
        dsV.close()
        
    elif function == "info":
        getInfo(ds)
