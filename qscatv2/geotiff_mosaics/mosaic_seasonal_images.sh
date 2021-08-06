#!/bin/bash

# for each year/month mosaic the regional geotiffs to form a single
# image

mosaic_ullr="-180.0 64.5 180.0 -58.0"

for year in `seq 1999 2009`
do
    if [ ${year} -eq 1999 ]
    then
        quarters="JAS OND"
    else
        quarters="JFM AMJ JAS OND"
    fi
    for quarter in ${quarters}
    do
        echo ${year} ${quarter}
        filelist=`ls *_quev_mean_db_${year}_${quarter}.tif`
        outfile=qscat_quev_mean_db_${year}_${quarter}.tif
        gdal_merge.py -o ${outfile} -of GTiff \
                      -n -9999. -a_nodata -9999. \
                      -ul_lr ${mosaic_ullr} ${filelist}
        filelist=`ls *_quev_std_db_${year}_${quarter}.tif`
        outfile=qscat_quev_std_db_${year}_${quarter}.tif
        gdal_merge.py -o ${outfile} -of GTiff \
                      -n -9999. -a_nodata -9999. \
                      -ul_lr ${mosaic_ullr} ${filelist}
    done
done
