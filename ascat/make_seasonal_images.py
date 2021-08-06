#!/usr/bin/env python

# script to make quarterly means of 5-day images.  Note
# that the 5-day image overlap in time periods.

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
Q2M = {
    "JAS": list(range(7, 10)),
    "OND": list(range(10, 13)),
    "JFM": list(range(1, 4)),
    "AMJ": list(range(4, 7)),
}

# this allows GDAL to throw Python Exceptions
gdal.UseExceptions()


def db2pr(dbvalue):
    pr = 10 ** (dbvalue / 10.0)
    return pr


if __name__ == "__main__":

    # set up arguments
    parser = argparse.ArgumentParser(
        "script to make quarterly " + "means of ascat dB values"
    )

    parser.add_argument(
        "-v",
        "--verbose",
        help="increase output verbosity",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-q",
        "--quarter",
        nargs="?",
        choices=("JAS", "OND", "JFM", "AMJ"),
        default="JAS",
        const="JAS",
        help="Quarter for aggregation. Default=JAS",
    )

    parser.add_argument("region", help="BYU region string (e.g. SAm, NAm, Ama, etc.)")
    parser.add_argument(
        "year", type=int, help="Year e.g. 2007 (ascat data start in 2007)"
    )

    args = parser.parse_args()

    verbose = args.verbose
    year = args.year
    quarter = args.quarter

    if year < 2007:
        print("Invalid year for ASCAT: should be 2007-2020")
        sys.exit(0)

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
        print("quarter: {}".format(quarter))

    # set data dir
    indir = os.path.join(DATADIR, "geotiffs", region, str(year))
    outdir = indir
    year2 = "{:02d}".format(year - 2000)

    monthlist = Q2M[quarter]

    # make a list of files for this year
    filepatt = "msfa-a-{}{}-*.tif".format(region, year2)
    globpatt = os.path.join(indir, filepatt)
    if verbose:
        print("glob pattern: {}".format(globpatt))
    filelist = glob.glob(globpatt)

    qlist = []
    for filepath in filelist:
        fn = os.path.basename(filepath)
        if verbose:
            print(fn)
        fn_dt = sp2.fn2dt(fn, date_flag="center")
        iyear = fn_dt.year
        imonth = fn_dt.month
        iday = fn_dt.day
        if imonth in monthlist:
            qlist.append(fn)
            if verbose:
                print("{}: {}-{}-{}".format(fn, iyear, imonth, iday))

    print("{}-{}: {}".format(year, quarter, qlist))

    if len(qlist) == 0:
        warnmsg = "No images found for this quarter.\n"
        sys.stdout.write(warnmsg)
        sys.exit(0)

    db_quarter = []
    for i, image in enumerate(qlist):
        a_imgpath = os.path.join(indir, image)
        try:
            a_ds = gdal.Open(a_imgpath)
        except RuntimeError:
            print("Unable to open {}".format(a_imgpath))
            sys.exit(1)

        try:
            srcband = a_ds.GetRasterBand(1)
        except RuntimeError:
            print("Band ({}) not found".format(1))
            sys.exit(1)

        a_data = srcband.ReadAsArray()
        a_mask = a_data == NODATA_VALUE

        # if this is the first image get projection and geotransform
        if i == 0:
            prj = a_ds.GetProjection()
            gt = a_ds.GetGeoTransform()
            ny, nx = a_data.shape

        db_data = a_data
        db_masked = np.ma.MaskedArray(db_data, a_mask)

        # add image to db_quarter array
        db_quarter.append(db_masked)

        # close datasets
        a_ds = None

    # convert list to array
    dbarray = np.ma.stack(db_quarter, axis=2)
    dbmean = np.ma.mean(dbarray, axis=2)
    dbstd = np.ma.std(dbarray, axis=2)
    print(dbmean.shape)

    # finally, save as a geotiff
    output_format = "GTiff"
    driver = gdal.GetDriverByName(output_format)
    dst_filename = "{}-msfa-mean-db-{}-{}.tif".format(region, year, quarter)
    dst_dir = os.path.join(DATADIR, "geotiffs", region, str(year))
    dst_path = os.path.join(dst_dir, dst_filename)
    if verbose:
        print("Output file: {}".format(dst_path))

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

    print("Quarterly ({}) Mean Stats".format(quarter))
    print("  Min: {}".format(dbmean_min))
    print("  Max: {}".format(dbmean_max))
    print("  Median: {}".format(dbmean_median))

    # repeat for standard deviation
    output_format = "GTiff"
    driver = gdal.GetDriverByName(output_format)
    dst_filename = "{}-msfa-std-db-{}-{}.tif".format(region, year, quarter)
    dst_dir = os.path.join(DATADIR, "geotiffs", region, str(year))
    dst_path = os.path.join(dst_dir, dst_filename)
    if verbose:
        print("Output file: {}".format(dst_path))

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

    print("Quarterly ({}) Stddev Stats".format(quarter))
    print("  Min: {}".format(dbstd_min))
    print("  Max: {}".format(dbstd_max))
    print("  Median: {}".format(dbstd_median))
