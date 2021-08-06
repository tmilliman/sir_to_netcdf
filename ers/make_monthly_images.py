#!/usr/bin/env python

# script to make monthly means of 17-day ERS1/2 images.

from __future__ import print_function

import os
import sys
import glob
import numpy as np
import sirpy2 as sp2
import argparse
from osgeo import gdal

DATADIR = "./"
NODATA_VALUE = -9999.0

# this allows GDAL to throw Python Exceptions
gdal.UseExceptions()


def db2pr(dbvalue):
    pr = 10 ** (dbvalue / 10.0)
    return pr


if __name__ == "__main__":

    # set up arguments
    parser = argparse.ArgumentParser(
        "script to make monthly " + "means and stdevs of ers dB values"
    )

    parser.add_argument(
        "-v",
        "--verbose",
        help="increase output verbosity",
        action="store_true",
        default=False,
    )

    parser.add_argument("region", help="BYU region string (e.g. SAm, NAm, Ama, etc.)")
    parser.add_argument(
        "year", type=int, help="Year e.g. 1992 (ers data start in 1992)"
    )
    parser.add_argument("month", type=int, help="Month (1-12)")

    args = parser.parse_args()

    verbose = args.verbose
    year = args.year
    month = args.month

    if (year < 1992) or (year > 2000):
        print("Invalid year for ERS1/2: 1992-2000")
        sys.exit(0)

    # set data type -
    if year < 1996:
        datatype = "ers1"
    elif year == 1996 and month < 5:
        datatype = "ers1"
    else:
        datatype = "ers2"

    # region list (LAEA regions only)
    valid_region_list = [
        "Grn",
        "Ala",
        "CAm",
        "NAm",
        "SAm",
        "NAf",
        "SAf",
        "Sib",
        "Eur",
        "SAs",
        "ChJ",
        "Ind",
        "Aus",
        "Ber",
    ]
    region = args.region
    try:
        region_index = valid_region_list.index(region)
    except Exception:
        sys.stderr.write("Region not valid.\n")
        sys.stderr.write("Valid regions are:\n")
        sys.stderr.write("{}\n".format(valid_region_list))
        sys.exit(1)

    if verbose:
        print("region: {}".format(region))
        print("year: {}".format(year))
        print("month: {}".format(month))

    indir = os.path.join(DATADIR, "geotiffs", region, str(year))
    outdir = indir
    if year == 2000:
        year2 = "00"
    else:
        year2 = "{:02d}".format(year - 1900)

    filepatt = "{}-a-{}{}-*.tif".format(datatype, region, year2)
    globpatt = os.path.join(indir, filepatt)
    if verbose:
        print("glob pattern: {}".format(globpatt))
    filelist = glob.glob(globpatt)

    # make a list of files for this month
    monthlist = []
    for filepath in filelist:
        fn = os.path.basename(filepath)
        fn_dt = sp2.fn2dt(fn, date_flag="center")
        iyear = fn_dt.year
        imonth = fn_dt.month
        iday = fn_dt.day
        if imonth == month:
            monthlist.append(fn)
            if verbose:
                print("{}: {}-{}-{}".format(fn, iyear, imonth, iday))

    print("{}-{:02d}: {}".format(year, month, monthlist))

    # loop over images for this month
    db_month = []
    for i, image in enumerate(monthlist):
        a_imgpath = os.path.join(indir, image)

        try:
            a_ds = gdal.Open(a_imgpath)

        except RuntimeError as e:
            print("Unable to open {}".format(a_imgpath))
            print(e)
            sys.exit(1)

        try:
            srcband = a_ds.GetRasterBand(1)

        except RuntimeError as e:
            # for example, try GetRasterBand(10)
            print("Band ({}) not found".format(1))
            print(e)
            sys.exit(1)

        a_data = srcband.ReadAsArray()
        a_mask = a_data == NODATA_VALUE

        # create masked array
        a_ma_data = np.ma.masked_array(a_data, mask=a_mask)

        # if this is the first image get projection and geotransform
        if i == 0:
            prj = a_ds.GetProjection()
            gt = a_ds.GetGeoTransform()
            ny, nx = a_data.shape

        # add masked array to db_month list
        db_month.append(a_ma_data)

        # close datasets
        a_ds = None

    # stack list into array and find mean
    dbarray = np.ma.stack(db_month, axis=2)
    dbmean = np.ma.mean(dbarray, axis=2)
    dbstd = np.ma.std(dbarray, axis=2)

    print(dbmean.shape)

    # finally, save mean sig0 as a geotiff
    output_format = "GTiff"
    driver = gdal.GetDriverByName(output_format)
    dst_filename = "{}-{}-monthly-mean-db-{}-{:02d}.tif"
    dst_filename = dst_filename.format(region, datatype, year, month)
    dst_dir = os.path.join(DATADIR, "geotiffs", region, str(year))
    dst_path = os.path.join(dst_dir, dst_filename)
    if verbose:
        print("Output file for sig0 means: {}".format(dst_path))

    dst_ds = driver.Create(dst_path, nx, ny, 1, gdal.GDT_Float32)
    dst_data = np.ma.filled(dbmean, fill_value=NODATA_VALUE)
    dst_ds.GetRasterBand(1).WriteArray(dst_data)
    dst_ds.GetRasterBand(1).SetNoDataValue(NODATA_VALUE)
    print("gt: {}".format(gt))
    dst_ds.SetGeoTransform(gt)
    dst_ds.SetProjection(prj)
    dst_ds = None

    dbmean_min = dbmean.min()
    dbmean_max = dbmean.max()
    dbmean_median = np.ma.median(dbmean)

    print("Monthly Mean Sig0 Stats")
    print("  Min: {}".format(dbmean_min))
    print("  Max: {}".format(dbmean_max))
    print("  Median: {}".format(dbmean_median))

    # and repeat for standard deviations
    output_format = "GTiff"
    driver = gdal.GetDriverByName(output_format)
    dst_filename = "{}-{}-monthly-std-db-{}-{:02d}.tif"
    dst_filename = dst_filename.format(region, datatype, year, month)
    dst_dir = os.path.join(DATADIR, "geotiffs", region, str(year))
    dst_path = os.path.join(dst_dir, dst_filename)
    if verbose:
        print("Output file for sig0 stdevs: {}".format(dst_path))

    dst_ds = driver.Create(dst_path, nx, ny, 1, gdal.GDT_Float32)
    dst_data = np.ma.filled(dbstd, fill_value=NODATA_VALUE)
    dst_ds.GetRasterBand(1).WriteArray(dst_data)
    dst_ds.GetRasterBand(1).SetNoDataValue(NODATA_VALUE)
    print("gt: {}".format(gt))
    dst_ds.SetGeoTransform(gt)
    dst_ds.SetProjection(prj)
    dst_ds = None

    dbstd_min = dbstd.min()
    dbstd_max = dbstd.max()
    dbstd_median = np.ma.median(dbstd)

    print("Monthly Sig0 Stdev Stats")
    print("  Min: {}".format(dbstd_min))
    print("  Max: {}".format(dbstd_max))
    print("  Median: {}".format(dbstd_median))
