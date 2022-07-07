#!/bin/bash

# for each year/month mosaic the regional geotiffs to form a single
# image

mosaic_ullr="-180.0 64.5 180.0 -58.0"

for year in `seq 1999 2009`
do
    # shortyear=`echo ${year} | cut -c3,4`
    if [ ${year} -eq 1999 ]
    then
        start_month=7
        end_month=12
    elif [ ${year} -eq 2009 ]
    then
        start_month=1
        end_month=11
    else
        start_month=1
        end_month=12
    fi
    for month in `seq -f '%02g' ${start_month} ${end_month}`
    do
        echo ${year} ${month}
        filelist=`ls *_qscat_quev_mean_db_${year}_${month}.tif`
        outfile=qscat_quev_mean_db_${year}_${month}.tif
        gdal_merge.py -o ${outfile} -of GTiff \
                      -n -9999. -a_nodata -9999. \
                      -ul_lr ${mosaic_ullr} \
                      -co COMPRESS=DEFLATE \
                      -co PREDICTOR=2 ${filelist}
        filelist=`ls *_qscat_quev_std_db_${year}_${month}.tif`
        outfile=qscat_quev_std_db_${year}_${month}.tif
        gdal_merge.py -o ${outfile} -of GTiff \
                      -n -9999. -a_nodata -9999. \
                      -ul_lr ${mosaic_ullr} \
                      -co COMPRESS=DEFLATE \
                      -co PREDICTOR=2 ${filelist}
    done
done
