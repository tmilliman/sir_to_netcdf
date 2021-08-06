#!/usr/bin/env python

"""
script to crawl the BYU/SCP archive for data and
replicate the structure here.

Here's a command to get a single file:

ncftpget ftp://ftp.scp.byu.edu/data/ascat/2009/sir/mafa/SAm/001/a/mafa-a-SAm09-001-005.sir.gz
"""
from __future__ import print_function

import os
import sys
import errno
import argparse
from datetime import datetime

dt_today = datetime.today()
current_year = dt_today.year
current_doy = datetime.now().timetuple().tm_yday


# function to make a directory tree
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description=(
            "print a list of ncftpget commands to pull images from " + "ftp.scp.byu.edu"
        )
    )

    parser.add_argument("region", help="BYU region string (e.g. SAm, NAm, Ama, etc.)")
    parser.add_argument("datatype", help="msfa, mafa, mdfa")
    parser.add_argument("year", type=int, help="4-digit year 2007-current_year")
    args = parser.parse_args()

    # check arguments

    # region
    valid_region_list = [
        "Ant",
        "Arc",
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
        "Ama",
    ]
    region = args.region
    try:
        region_index = valid_region_list.index(region)
    except Exception:
        sys.stderr.write("Region not valid")
        sys.exit(1)

    # year
    year = args.year
    if (year < 2007) or (year > current_year):
        sys.stderr.write("Year must be between 2009 and current year")
        sys.exit(1)

    # data type - only accept ones valid for all regions
    # polar regions have additional data types for morning, noon,
    # and evening passes
    valid_datatype_list = ["msfa", "mafa", "mdfa"]

    data_type = args.datatype
    try:
        datatype_index = valid_datatype_list.index(data_type)
    except Exception:
        sys.stderr.write("Data type not valid")
        sys.exit(1)

    # for testing set these here
    remote_host = "ftp.scp.byu.edu"
    basepath = "/data/ascat"
    # year = 2009
    # region = 'Ama'
    # data_type = 'mafa'
    itype_list = ["a"]

    # first make tree for this year, region, data_type
    remote_region_path = os.path.join(
        basepath, "{0}".format(year), "sir", data_type, region
    )

    # and equivalent for local
    local_region_path = os.path.join("./", "{0}".format(year), "sir", data_type, region)

    start_doy = 1

    # go to end of year unless we're looking for current year
    if year == current_year:
        last_doy = current_doy
    else:
        last_doy = 365

    # get 2-digit year
    sy = year - 2000

    short_year = "{0:02d}".format(sy)

    # unlike the qscat and oscat data the ascat data composites
    # for 5-days but repeats every 3rd day.  So composite days are:
    #
    #  001-005
    #  003-007
    #  005-009
    #  .
    #  .
    #  .
    #
    ncomp = 5
    nfreq = 2
    doy_list = range(start_doy, last_doy, nfreq)

    for doy in doy_list:

        doy_str = "{0:03d}".format(doy)
        end_doy = doy + ncomp - 1

        for itype in itype_list:
            i_file = "{0}-{1}-{2}{3}-{4:03d}-{5:03d}.sir.gz".format(
                data_type, itype, region, short_year, doy, end_doy
            )

            path_remote = os.path.join(remote_region_path, doy_str, itype, i_file)
            path_local = os.path.join(local_region_path, doy_str, itype, i_file)

            # make sure local directory exists
            dir_local = os.path.join(local_region_path, doy_str, itype)
            mkdir_p(dir_local)

            cmdstr = "ncftpget -C {0} {1} {2}".format(
                remote_host, path_remote, path_local
            )

            print(cmdstr)
