#!/usr/bin/env python

import sys
import glob
from datetime import datetime
import argparse

import pandas as pd
import xarray as xr

import ers_common as common


def time_index_from_filenames(filenames):
    return pd.DatetimeIndex(
        [pd.Timestamp(f[17:21] + f[22:24] + "15") for f in filenames]
    )


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Create ERS1/2 monthly mean netcdf file"
    )

    args = parser.parse_args()

    # get list of files
    filepattern = "ers_ers[12]_mean_db_*_[01][0-9].tif"
    filenames = glob.glob(filepattern)
    filelist = filenames
    time = xr.Variable("time", time_index_from_filenames(filelist))

    nimages = len(filelist)
    print("Number of images: {}".format(nimages))

    if nimages == 0:
        print("No images found.")
        sys.exit(0)

    # concat all the files with the time index
    da = xr.concat([xr.open_rasterio(f) for f in filelist], dim=time)

    # remove band dimension (each input image has a single band)
    da = da.squeeze("band", drop=True)

    # rename coords
    da_ll = da.rename({"y": "lat", "x": "lon"})

    # create to a data set
    ds = da_ll.to_dataset(name="sig0")

    # set attributes for dataset
    # ds.attrs['Conventions'] = "None"
    ds.attrs["title"] = "ERS1/2 sigma-0 Monthly Mean"
    ds.attrs["description"] = "ERS1/2 monthly mean ers1/2 sigma-0"
    ds.attrs["history"] = str(datetime.utcnow()) + " Python/xarray"
    ds.attrs["source"] = "NASA Scatterometer Climate Record Pathfinder"
    ds.attrs["references"] = "https://www.scp.byu.edu/"
    ds.attrs["comment"] = "Preliminary"

    # set attributes for dims
    ds.lon.attrs["axis"] = "X"
    ds.lon.attrs["standard_name"] = "longitude"
    ds.lon.attrs["long_name"] = "longitude"
    ds.lon.attrs["units"] = "degrees_east"

    ds.lat.attrs["axis"] = "Y"
    ds.lat.attrs["standard_name"] = "latitude"
    ds.lat.attrs["long_name"] = "latitude"
    ds.lat.attrs["units"] = "degrees_north"

    ds.time.attrs["axis"] = "T"
    ds.time.attrs["standard_name"] = "time"
    ds.time.attrs["long_name"] = "time"

    # set attributes for vars
    ds.sig0.attrs["units"] = "decibel"
    ds.sig0.attrs["standard_name"] = "sigma0"
    ds.sig0.attrs["long_name"] = "surface normalized radar backscatter coefficient"
    ds.sig0.attrs["missing_value"] = -9999.0
    ds.sig0.attrs["_FillValue"] = -9999.0
    ds.sig0.attrs["valid_min"] = -33.0
    ds.sig0.attrs["valid_max"] = 0.0

    print(ds)

    encoding = common.encoding_sig0

    outfile = "ERS_monthly_land_sig0_mean.nc"
    ds.to_netcdf(outfile, format="NETCDF4", encoding=encoding, unlimited_dims=["time"])
