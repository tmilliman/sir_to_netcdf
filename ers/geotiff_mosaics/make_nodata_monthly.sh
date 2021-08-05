#!/bin/bash

# script to make an image with nodata to cover gaps in the
# data availability

infile=ers_ers1_mean_db_1993_01.tif
outfile=ers_missing_data_month.tif

gdal_calc.py -A ${infile} \
             --calc="(A>-9999)*-9999" \
             --NoDataValue=-9999. \
             --outfile=${outfile}
