#!/usr/bin/env python

import sys
import os
from datetime import datetime
import argparse

import pandas as pd
import xarray as xr

import ascat_common as common


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Create ASCAT masked seasonal sig0 std netcdf"
    )

    args = parser.parse_args()

    season_list = ["JFM", "AMJ", "JAS", "OND"]

    # make a file list of seasonal std geotiffs in time order
    filelist = []
    times = []
    for year in range(common.START_YEAR, common.END_YEAR + 1):
        for season in season_list:
            toffset = common.MDSWITCH[season]
            fname = "ascat_msfa_std_db_{}_{}_masked_{}.tif"
            fname = fname.format(year, season, common.GHSMIN)
            if os.path.exists(fname):
                filelist.append(fname)
            timestamp = pd.Timestamp("{}".format(year) + toffset)
            times.append(timestamp)

    nimages = len(filelist)
    print("Number of Images: {}".format(nimages))

    if nimages == 0:
        print("No images found.")
        sys.exit(0)

    time = xr.Variable("time", pd.DatetimeIndex(times))
    da = xr.concat([xr.open_rasterio(f) for f in filelist], dim=time)

    # remove band dimension (each input image has a single band)
    da = da.squeeze("band", drop=True)

    # rename coords
    da_ll = da.rename({"y": "lat", "x": "lon"})

    # convert to data set
    ds = da_ll.to_dataset(name="sig0std")

    # set attributes for dataset
    # ds.attrs['Conventions'] = "None"
    ds.attrs["title"] = "ASCAT sigma-0 Masked seasonal Std. Dev."
    ds.attrs["description"] = (
        "ASCAT std from seasonal mean msfa sigma-0 with " + "urban and water masks"
    )
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
    ds.sig0std.attrs["units"] = "decibel"
    ds.sig0std.attrs["standard_name"] = "sigma0-std"
    ds.sig0std.attrs[
        "long_name"
    ] = "standard deviation of surface normalized radar backscatter coefficient"
    ds.sig0std.attrs["missing_value"] = -9999.0
    ds.sig0std.attrs["_FillValue"] = -9999.0
    ds.sig0std.attrs["valid_min"] = 0.0

    print(ds)

    encoding = common.encoding_sig0std

    outfile = "ASCAT_seasonal_urban_sig0_StdDev.nc"
    ds.to_netcdf(outfile, format="NETCDF4", encoding=encoding, unlimited_dims=["time"])
