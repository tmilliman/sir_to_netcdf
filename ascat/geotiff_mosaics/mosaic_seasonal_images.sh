#!/bin/bash

# for each year/month mosaic the regional geotiffs to form a single
# image

mosaic_ullr="-180.0 64.5 180.0 -58.0"

for year in `seq 2007 2020`
do
    # shortyear=`echo ${year} | cut -c3,4`
    quarters="JFM AMJ JAS OND"
    for quarter in ${quarters}
    do
        echo ${year} ${quarter}
        filelist=`ls *_msfa_mean_db_${year}_${quarter}.tif`
        outfile=ascat_msfa_mean_db_${year}_${quarter}.tif
        gdal_merge.py -o ${outfile} -of GTiff \
                      -n -9999. -a_nodata -9999. \
                      -ul_lr ${mosaic_ullr} \
                      -co COMPRESS=DEFLATE \
                      -co PREDICTOR=2 ${filelist}
        filelist=`ls *_msfa_std_db_${year}_${quarter}.tif`
        outfile=ascat_msfa_std_db_${year}_${quarter}.tif
        gdal_merge.py -o ${outfile} -of GTiff \
                      -n -9999. -a_nodata -9999. \
                      -ul_lr ${mosaic_ullr} \
                      -co COMPRESS=DEFLATE \
                      -co PREDICTOR=2 ${filelist}
    done
done
        
