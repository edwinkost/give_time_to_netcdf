#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

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
    lat = out_rootgrp.createVariable('lat', 'f4', ('lat', ))
    lat.long_name = 'latitude'
    lat.units = 'degrees_north'
    lat.standard_name = 'latitude'
    lat[:] = latitudes

    # create longitude
    lon = out_rootgrp.createVariable('lon', 'f4', ('lon', ))
    lon.long_name = 'longitude'
    lon.units = 'degrees_east'
    lon.standard_name = 'longitude'
    lon[:] = longitudes

    # create variables
    shortVarName = variable_short_name 
    longVarName  = inp_rootgrp.variables[variable_short_name].long_name
    var = rootgrp.createVariable(shortVarName, 'f4', ('time', 'lat', 'lon',), fill_value = inp_rootgrp.variables["Band1"]._FillValue, zlib = zlib_option)
    var.standard_name = varName
    var.long_name = variable_short_name
    var.units = varUnits

    # important attributes needed to be copied
    attribute_keys = ['institution', 'title', 'description', 'history']
    for key in attribute_keys:
        try:
            setattr(out_rootgrp, key, vars(inp_rootgrp)[key])
        except:
            pass
    
    # syncing and closing output netcdf file
    out_rootgrp.sync()
    out_rootgrp.close()

    
    # UNTIL THIS PART
    
    # copying data to 
    def data2NetCDF(self, ncFileName, shortVarName, varField, timeStamp, posCnt = None):

        rootgrp = nc.Dataset(ncFileName,'a')

        date_time = rootgrp.variables['time']
        if posCnt == None: posCnt = len(date_time)
        date_time[posCnt] = nc.date2num(timeStamp,date_time.units,date_time.calendar)

        rootgrp.variables[shortVarName][posCnt,:,:] = varField

        rootgrp.sync()
        rootgrp.close()



if __name__ == '__main__':
    sys.exit(main())
