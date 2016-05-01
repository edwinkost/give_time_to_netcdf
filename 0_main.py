#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import datetime

import numpy as np
import pcraster as pcr
import netCDF4 as nc

###########################################################################################################

def main():
    
    # input and output files:
    inp_file = os.path.abspath(sys.argv[1])
    out_file = os.path.abspath(sys.argv[2])
    
    # variable short name that will be used/copied
    variable_short_name = str(sys.argv[3])
    
    # date and time that will be assigned
    date_string = str(sys.argv[4])
    time_string = "00:00:00"
    
    # compression option
    zlib_option = True
    
    # open input file
    inp_rootgrp = nc.Dataset(inp_file)
    
    # reading latitudes and longitudes
    try:
        latitudes  = inp_rootgrp.variables['lat'][:]
        longitudes = inp_rootgrp.variables['lon'][:]
    except:
        latitudes  = inp_rootgrp.variables['latitude'][:]
        longitudes = inp_rootgrp.variables['longitude'][:]

    # make output file
    out_rootgrp = nc.Dataset(out_file, 'w', format = inp_rootgrp.file_format)

    # create time
    out_rootgrp.createDimension('time', None)
    date_time = out_rootgrp.createVariable('time', 'f4', ('time', ))
    date_time.standard_name = 'time'
    date_time.long_name = 'Days since 1901-01-01'
    date_time.units     = 'Days since 1901-01-01' 
    date_time.calendar  = 'standard'

    # create latitude
    out_rootgrp.createDimension('lat', len(latitudes))
    lat = out_rootgrp.createVariable('lat', 'f4', ('lat', ))
    lat.long_name = 'latitude'
    lat.units = 'degrees_north'
    lat.standard_name = 'latitude'
    lat[:] = latitudes

    # create longitude
    out_rootgrp.createDimension('lon', len(longitudes))
    lon = out_rootgrp.createVariable('lon', 'f4', ('lon', ))
    lon.long_name = 'longitude'
    lon.units = 'degrees_east'
    lon.standard_name = 'longitude'
    lon[:] = longitudes

    # create variables
    shortVarName = variable_short_name 
    longVarName  = inp_rootgrp.variables[variable_short_name].long_name
    var = out_rootgrp.createVariable(shortVarName, 'f4', ('time', 'lat', 'lon',), fill_value = inp_rootgrp.variables["Band1"]._FillValue, zlib = zlib_option)
    var.standard_name = shortVarName
    var.long_name = longVarName
    try:
        var.units = inp_rootgrp.variables[variable_short_name].units
    except:
        pass # or var.units = 1
		
    # important attributes needed to be copied
    attribute_keys = ['institution', 'title', 'description', 'history']
    for key in attribute_keys:
        try:
            setattr(out_rootgrp, key, vars(inp_rootgrp)[key])
        except:
            pass
    
    # copying data to a specific time
    date_used = str(date_string).split('-')
    if time_string == "00:00:00": time_used = int(0)
    time_stamp = datetime.datetime(int(date_used[0]), int(date_used[1]), int(date_used[2]), time_used)
    
    date_time = out_rootgrp.variables['time']
    posCnt = 0
    date_time[posCnt] = nc.date2num(time_stamp, date_time.units, date_time.calendar)
    out_rootgrp.variables[shortVarName][posCnt,:,:] = inp_rootgrp.variables[shortVarName][:,:]

    # syncing and closing output netcdf file
    out_rootgrp.sync()
    out_rootgrp.close()

    print("all done")

if __name__ == '__main__':
    sys.exit(main())
