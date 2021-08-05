#!/bin/bash

# script to collect all the monthly images from a region,
# reproject them to epsg:4326 

region=$1
if [ "${region}" == "" ]
then
    echo "Must specify region."
    exit
fi

. region_warp_extents.sh

# copy geotiffs in local LAEA projection
cp ../geotiffs/${region}/*/${region}-ers[12]-monthly-mean-db-*.tif ./
cp ../geotiffs/${region}/*/${region}-ers[12]-monthly-std-db-*.tif ./

# reproject to epsg:4326 and rename files

if [ "${region}" != "Ber" ]
then
    for file in `ls ${region}-ers[12]-monthly-mean-db-*.tif`
    do
        echo ${file}
        target=`echo ${file} | sed 's/ers\([12]\)-monthly/ers\1/' | sed 's/-/_/g'`
        gdalwarp -t_srs epsg:4326 -tr 0.05 0.05 -te ${warp_extent} -overwrite -tap -r average ${file} ${target}
        rm ${file}
    done

    # repeat for std
    for file in `ls ${region}-ers[12]-monthly-std-db-*.tif`
    do
        echo ${file}
        target=`echo ${file} | sed 's/ers\([12]\)-monthly/ers\1/' | sed 's/-/_/g'`
        gdalwarp -t_srs epsg:4326 -tr 0.05 0.05 -te ${warp_extent} -overwrite -tap -r average ${file} ${target}
        rm ${file}
    done
else
    # reproject and rename files
    for file in `ls ${region}-ers[12]-monthly-mean-db-*.tif`
    do
        echo ${file}
        target=`echo ${file} | sed 's/ers\([12]\)-monthly/ers\1/' | sed 's/-/_/g' | sed 's/\.tif/\_1\.tif/'`
        gdalwarp -t_srs epsg:4326 -tr 0.05 0.05 -te ${warp_extent1} -overwrite -tap -r average ${file} ${target}
        target=`echo ${target} | sed 's/_1\.tif/\_2\.tif/'`
        gdalwarp -t_srs epsg:4326 -tr 0.05 0.05 -te ${warp_extent2} -overwrite -tap -r average ${file} ${target}
        rm ${file}
    done

    # repeat for std
    for file in `ls ${region}-ers[12]-monthly-std-db-*.tif`
    do
        echo ${file}
        target=`echo ${file} | sed 's/ers\([12]\)-monthly/ers\1/' | sed 's/-/_/g' | sed 's/\.tif/\_1\.tif/'`
        gdalwarp -t_srs epsg:4326 -tr 0.05 0.05 -te ${warp_extent1} -overwrite -tap -r average ${file} ${target}
        target=`echo ${target} | sed 's/_1\.tif/\_2\.tif/'`
        gdalwarp -t_srs epsg:4326 -tr 0.05 0.05 -te ${warp_extent2} -overwrite -tap -r average ${file} ${target}
        rm ${file}
    done
    
fi
    
