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
