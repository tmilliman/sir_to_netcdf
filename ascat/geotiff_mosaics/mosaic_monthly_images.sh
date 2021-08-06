#!/bin/bash

# for each year/month mosaic the regional geotiffs to form a single
# image

mosaic_ullr="-180.0 64.5 180.0 -58.0"

for year in `seq 2007 2020`
do
    # shortyear=`echo ${year} | cut -c3,4`
    start_month=1
    end_month=12
    for month in `seq -f '%02g' ${start_month} ${end_month}`
    do
        echo ${year} ${month}
        filelist=`ls *_ascat_msfa_mean_db_${year}_${month}.tif`
        outfile=ascat_msfa_mean_db_${year}_${month}.tif
        gdal_merge.py -o ${outfile} -of GTiff \
                      -n -9999. -a_nodata -9999. \
                      -ul_lr ${mosaic_ullr} \
                      -co COMPRESS=DEFLATE \
                      -co PREDICTOR=2 ${filelist}
        filelist=`ls *_ascat_msfa_std_db_${year}_${month}.tif`
        outfile=ascat_msfa_std_db_${year}_${month}.tif
        gdal_merge.py -o ${outfile} -of GTiff \
                      -n -9999. -a_nodata -9999. \
                      -ul_lr ${mosaic_ullr} \
                      -co COMPRESS=DEFLATE \
                      -co PREDICTOR=2 ${filelist}
    done
done
