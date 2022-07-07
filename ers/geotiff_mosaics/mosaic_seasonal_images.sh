#!/bin/bash

# for each year/quarter mosaic the regional geotiffs to form a single
# image

mosaic_ullr="-180. 64.5 180. -58.0"

# Treat ERS1/2 as combined for seasons
for year in `seq 1993 2000`
do
    for quarter in JFM AMJ JAS OND
    do
        echo ${year} ${quarter}

        # merge regional mean images
        filelist=`ls *_ers_mean_db_${year}_${quarter}.tif`
        outfile=ers_ers12_mean_db_${year}_${quarter}.tif
        if [ -f ${outfile} ]
        then
            rm ${outfile}
        fi
        gdal_merge.py -o ${outfile} -of GTiff \
                      -n -9999. -a_nodata -9999. \
                      -ul_lr ${mosaic_ullr} \
                      -co COMPRESS=DEFLATE \
                      -co PREDICTOR=2 ${filelist}

        # repeat for std
        filelist=`ls *_ers_std_db_${year}_${quarter}.tif`
        outfile=ers_ers12_std_db_${year}_${quarter}.tif
        if [ -f ${outfile} ]
        then
            rm ${outfile}
        fi
        gdal_merge.py -o ${outfile} -of GTiff \
                      -n -9999. -a_nodata -9999. \
                      -ul_lr ${mosaic_ullr} \
                      -co COMPRESS=DEFLATE \
                      -co PREDICTOR=2 ${filelist}
    done
done
