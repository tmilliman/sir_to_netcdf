#!/usr/bin/env python

import sys
import glob
from datetime import datetime
import numpy as np
import pandas as pd
import xarray as xr
import rioxarray as rio

import qscat_common as common

def time_index_from_mean_filenames(filenames):
    return pd.DatetimeIndex(
        [pd.Timestamp(f[19:23] + f[24:26] + '15') for f in filenames]
    )


if __name__ == "__main__":

    # get list of files
    filepattern = "qscat_quev_mean_db_*_[01][0-9].tif"
    filenames = glob.glob(filepattern)
    filelist = filenames
    time = xr.Variable('time', time_index_from_mean_filenames(filelist))

    nimages = len(filelist)
    print("Number of images: {}".format(nimages))

    # concat all the files with the time index
    da = xr.concat([rio.open_rasterio(f) for f in filelist],
                   dim=time)
    
    # remove band dimension (each input image has a single band)
    da = da.squeeze('band', drop=True)

    # rename coords
    da_ll = da.rename({"y": "lat", "x": "lon"})

    # create to a data set
    ds = da_ll.to_dataset(name="sig0")

    # set attributes for dataset
    # ds.attrs['Conventions'] = "None"    
    ds.attrs['title'] = 'QuikSCAT sigma-0 Monthly Mean'
    ds.attrs['description'] = "QuikSCAT monthly mean quev sigma-0"    
    ds.attrs['history'] = str(datetime.utcnow()) + " Python/xarray"
    ds.attrs['source'] = "NASA Scatterometer Climate Record Pathfinder"
    ds.attrs['references'] = "https://www.scp.byu.edu/"
    ds.attrs['creator_email'] = 'thomas.milliman@unh.edu'
    ds.attrs['creator_name'] = 'Tom Milliman'
    ds.attrs['creator_type'] = 'person'
    ds.attrs['comment'] = "Preliminary"
    
    # set attributes for dims
    ds.lon.attrs['axis'] = 'X'
    ds.lon.attrs['standard_name'] = 'longitude'
    ds.lon.attrs['long_name'] = 'longitude'
    ds.lon.attrs['units'] = 'degrees_east'
    
    ds.lat.attrs['axis'] = 'Y'
    ds.lat.attrs['standard_name'] = 'latitude'
    ds.lat.attrs['long_name'] = 'latitude'
    ds.lat.attrs['units'] = 'degrees_north'

    ds.time.attrs['axis'] = 'T'
    ds.time.attrs['standard_name'] = 'time'
    ds.time.attrs['long_name'] = 'time'    
    
    # set attributes for vars
    ds.sig0.attrs['units'] = "decibel"
    ds.sig0.attrs['standard_name'] = "sigma0"
    ds.sig0.attrs['long_name'] = "surface normalized radar backscatter coefficient"
    ds.sig0.attrs['missing_value'] = -9999.
    ds.sig0.attrs['_FillValue'] = -9999.
    ds.sig0.attrs['valid_min'] = -33.
    ds.sig0.attrs['valid_max'] = 0.0
    
    print(ds)
    
    encoding = common.encoding_sig0
    
    outfile = "QuikSCAT_monthly_land_sig0_mean.nc"
    ds.to_netcdf(outfile, format="NETCDF4", encoding=encoding,
                 unlimited_dims=['time'])
