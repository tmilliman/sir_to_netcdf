#!/bin/bash

# script to collect all the monthly images from a region,
# reproject them to epsg:4326 and rename them for upload
# to google cloud storage

region=$1
if [ "${region}" == "" ]
then
    echo "Must specify region."
    exit
fi

. region_warp_extents.sh

# copy geotiffs in local LAEA projection
cp -p ../geotiffs/${region}/*/${region}-msfa-monthly-mean-db-*.tif ./
cp -p ../geotiffs/${region}/*/${region}-msfa-monthly-std-db-*.tif ./

if [ "${region}" != "Ber" ]
then
    # reproject and rename files
    for file in `ls ${region}-msfa-monthly-mean-db-*.tif`
    do
        echo ${file}
        target=`echo ${file} | sed 's/msfa-monthly/ascat-msfa/' | sed 's/-/_/g'`
        gdalwarp -t_srs epsg:4326 -tr 0.05 0.05 -te ${warp_extent} -overwrite -tap -r average ${file} ${target}
        rm ${file}
    done

    # repeat for std images
    for file in `ls ${region}-msfa-monthly-std-db-*.tif`
    do
        echo ${file}
        target=`echo ${file} | sed 's/msfa-monthly/ascat-msfa/' | sed 's/-/_/g'`
        gdalwarp -t_srs epsg:4326 -tr 0.05 0.05 -te ${warp_extent} -overwrite -tap -r average ${file} ${target}
        rm ${file}
    done
else
    # reproject and rename files
    for file in `ls ${region}-msfa-monthly-mean*.tif`
    do
        echo ${file}
        target=`echo ${file} | sed 's/msfa-monthly/ascat-msfa/' | sed 's/-/_/g' | sed 's/\.tif/\_1\.tif/'`
        gdalwarp -t_srs epsg:4326 -tr 0.05 0.05 -te ${warp_extent1} -overwrite -tap -r average ${file} ${target}
        target=`echo ${target} | sed 's/_1\.tif/\_2\.tif/'`
        gdalwarp -t_srs epsg:4326 -tr 0.05 0.05 -te ${warp_extent2} -overwrite -tap -r average ${file} ${target}
        rm ${file}
    done

    # repeat for std images
    for file in `ls ${region}-msfa-monthly-std-db*.tif`
    do
        echo ${file}
        target=`echo ${file} | sed 's/msfa-monthly/ascat-msfa/' | sed 's/-/_/g' | sed 's/\.tif/\_1\.tif/'`
        gdalwarp -t_srs epsg:4326 -tr 0.05 0.05 -te ${warp_extent1} -overwrite -tap -r average ${file} ${target}
        target=`echo ${target} | sed 's/_1\.tif/\_2\.tif/'`
        gdalwarp -t_srs epsg:4326 -tr 0.05 0.05 -te ${warp_extent2} -overwrite -tap -r average ${file} ${target}
        rm ${file}
    done
fi
