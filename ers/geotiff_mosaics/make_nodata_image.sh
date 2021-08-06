#!/bin/bash

# script to make an image with nodata to cover gaps in the
# data availability

infile=ers_ers12_mean_db_1993_JFM.tif
outfile=ers_missing_data_image.tif

gdal_calc.py -A ${infile} \
             --calc="(A>-9999)*-9999" \
             --NoDataValue=-9999. \
             --outfile=${outfile}
