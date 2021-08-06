#!/bin/bash

# script to make an image with nodata to cover gaps in the
# data availability

infile=qscat_quev_mean_db_1999_JAS.tif
outfile=qscat_missing_data_image.tif

gdal_calc.py -A ${infile} \
             --calc="(A>-9999)*-9999" \
             --NoDataValue=-9999. \
             --outfile=${outfile}
