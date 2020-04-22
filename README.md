# NetCDF Utils

This repository host a set of utilities to deal with NetCDF files.

## Area visualisation

To view the area considered by a NetCDF file:

```$ python3 map_visualiser.py --inputFile=MyFile.nc --latVariable=lat --lonVariable=lon --function=boundaries```

## Winds visualisation

To view the area considered by a NetCDF file:

```$ python3 map_visualiser.py --inputFile=MyFile.nc --latVariable=lat --lonVariable=lon --function=winds --plotVariable=U10M```

## Currents visualisation

To view the area considered by a NetCDF file:

```$ python3 map_visualiser.py --inputFile=MyFile.nc --latVariable=lat --lonVariable=lon --function=currents --plotVariable=votemper```

## Convert Medslik-II txt output to NetCDF files

First, we convert the file to CSV, to be comfortable during the creation of the NetCDF. Note: this script has to be replaced with a few lines in the python script.

```$ txt_to_csv.sh mdktxt_samples/relo19080520.rel mdktxt_samples/relo19080520.csv```

Then, we invoke the python script to obtain the NetCDF:

```$ python  mdktxt_to_nc.py --inputFile=mdktxt_samples/relo19080520.csv --outputFile=mdktxt_samples/relo19080520.nc --time="2019-08-05 20:00"```