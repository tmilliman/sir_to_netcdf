#!/bin/bash

# script to make an image with nodata to cover gaps in the
# data availability

infile=ascat_msfa_mean_db_2007_01.tif
outfile=ascat_missing_data_month.tif

gdal_calc.py -A ${infile} \
             --calc="(A>-9999)*-9999" \
             --NoDataValue=-9999. \
             --outfile=${outfile}
