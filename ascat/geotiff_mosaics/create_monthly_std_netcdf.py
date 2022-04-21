#!/usr/bin/env python

import glob
from datetime import datetime
import pandas as pd
import xarray as xr
import rioxarray as rio

import ascat_common as common


def time_index_from_filenames(filenames):
    return pd.DatetimeIndex(
        [pd.Timestamp(f[18:22] + f[23:25] + "15") for f in filenames]
    )


if __name__ == "__main__":

    # get list of files
    filepattern = "ascat_msfa_std_db_*_[01][0-9].tif"
    filenames = glob.glob(filepattern)
    filelist = filenames
    time = xr.Variable("time", time_index_from_filenames(filelist))

    nimages = len(filelist)
    print("Number of images: {}".format(nimages))

    # concat all the files with the time index
    da = xr.concat(
        [rio.open_rasterio(f, parse_coordinates=True) for f in filelist], dim=time
    )

    # remove band dimension (each input image has a single band)
    da = da.squeeze("band", drop=True)

    # rename coords
    da_ll = da.rename({"y": "lat", "x": "lon"})

    # convert to a data set
    ds = da_ll.to_dataset(name="sig0std")

    # set attributes for dataset
    # ds.attrs['Conventions'] = "None"
    ds.attrs["title"] = "ASCAT sigma-0 Monthly Std. Dev."
    ds.attrs["description"] = "ASCAT std from monthly mean msfa sigma-0"
    ds.attrs["history"] = str(datetime.utcnow()) + " Python/xarray"
    ds.attrs["source"] = "NASA Scatterometer Climate Record Pathfinder"
    ds.attrs["references"] = "https://www.scp.byu.edu/"
    ds.attrs["creator_email"] = "thomas.milliman@unh.edu"
    ds.attrs["creator_name"] = "Tom Milliman"
    ds.attrs["creator_type"] = "person"
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
    ds.sig0std.attrs["grid_mapping"] = "spatial_ref"
    ds.sig0std.attrs["standard_name"] = "sigma0-std"
    ds.sig0std.attrs["long_name"] = [
        "standard deviation surface normalized radar backscatter coefficient"
    ]
    ds.sig0std.attrs["missing_value"] = -9999.0
    ds.sig0std.attrs["_FillValue"] = -9999.0
    ds.sig0std.attrs["valid_min"] = 0.0
    ds.sig0std.attrs["coordinates"] = "spatial_ref"

    print(ds)

    encoding = common.encoding_sig0std

    outfile = "ASCAT_monthly_land_sig0_StdDev.nc"
    ds.to_netcdf(outfile, format="NETCDF4", encoding=encoding, unlimited_dims=["time"])
