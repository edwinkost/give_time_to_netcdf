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

    # UNTIL THIS PART
    
    # important attributes
    k = 
    v = 
    # TODO: copy also 
    attributeDictionary = self.attributeDictionary
    for k, v in attributeDictionary.items(): setattr(rootgrp,k,v)

    rootgrp.sync()
    rootgrp.close()


    


    # prepare logger and its directory
    log_file_location = output['folder'] + "/log/"
    try:
        os.makedirs(log_file_location)
    except:
        pass
    vos.initialize_logging(log_file_location)
    
    # time object
    modelTime = ModelTime() # timeStep info: year, month, day, doy, hour, etc
    modelTime.getStartEndTimeSteps(startDate, endDate)
    
    calculationModel = CalcFramework(cloneMapFileName,\
                                     input_files, \
                                     modelTime, \
                                     output)

    dynamic_framework = DynamicFramework(calculationModel, modelTime.nrOfTimeSteps)
    dynamic_framework.setQuiet(True)
    dynamic_framework.run()

if __name__ == '__main__':
    sys.exit(main())
