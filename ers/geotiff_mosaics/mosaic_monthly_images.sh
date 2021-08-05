#!/bin/bash

# for each year/month mosaic the regional geotiffs to form a single
# image

mosaic_ullr="-180.0 64.5 180.0 -58.0"

# first do ERS1
rm ers_ers1_mean_db_[12]*_[01][0-9].tif
rm ers_ers1_std_db_[12]*_[01][0-9].tif
for year in `seq 1993 1996`
do

    start_month=1
    if [ ${year} -eq 1996 ]
    then
        end_month=4
    else
        end_month=12
    fi

    echo "Start month: ${start_month}  End month: ${end_month}"

    for month in `seq -f '%02g' ${start_month} ${end_month}`
    do
        echo ${year} ${month}

        # merge regional mean images
        filelist=`ls *_ers1_mean_db_${year}_${month}.tif`
        export outfile=ers_ers1_mean_db_${year}_${month}.tif
        gdal_merge.py -o ${outfile} -of GTiff \
                      -n -9999. -a_nodata -9999. \
                      -ul_lr ${mosaic_ullr} ${filelist}

        # repeat for std
        filelist=`ls *_ers1_std_db_${year}_${month}.tif`
        export outfile=ers_ers1_std_db_${year}_${month}.tif
        /bin/rm -f ${outfile}
        gdal_merge.py -o ${outfile} -of GTiff \
                      -n -9999. -a_nodata -9999. \
                      -ul_lr ${mosaic_ullr} ${filelist}
    done
done

# then ERS2
rm ers_ers2_mean_db_[12]*_[01][0-9].tif
rm ers_ers2_std_db_[12]*_[01][0-9].tif
for year in `seq 1996 2000`
do
    # shortyear=`echo ${year} | cut -c3,4`
    if [ ${year} -eq 1996 ]
    then
        start_month=6
        end_month=12
    else
        start_month=1
        end_month=12
    fi

    for month in `seq -f '%02g' ${start_month} ${end_month}`
    do
        echo ${year} ${month}
        filelist=`ls *_ers2_mean_db_${year}_${month}.tif`
        outfile=ers_ers2_mean_db_${year}_${month}.tif
        gdal_merge.py -o ${outfile} -of GTiff \
                      -n -9999. -a_nodata -9999. \
                      -ul_lr ${mosaic_ullr} ${filelist}
        filelist=`ls *_ers2_std_db_${year}_${month}.tif`
        outfile=ers_ers2_std_db_${year}_${month}.tif
        gdal_merge.py -o ${outfile} -of GTiff \
                      -n -9999. -a_nodata -9999. \
                      -ul_lr ${mosaic_ullr} ${filelist}
    done
done

