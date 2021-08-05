#!/bin/bash

# apply combined GHS and WF mask

GHSMIN=20
WFMAX=50
mask="mask_GHS${GHSMIN}_WF${WFMAX}.tif"

for image in `ls ers_ers12_*_db_*_[JOA]*.tif`
do
    echo ${image}
    outfile=`basename ${image} .tif`_masked_${GHSMIN}.tif
    gdal_calc.py -A ${image} -B ${mask} \
                 --calc="A*B" \
                 --NoDataValue=-9999 \
                 --type=Float32 \
                 --overwrite \
                 --co COMPRESS=DEFLATE \
                 --co PREDICTOR=3 \
                 --outfile=${outfile}
done

# GHSMIN=10
# WFMAX=50
# mask="mask_GHS${GHSMIN}_WF${WFMAX}.tif"

# for image in `ls ers_ers12_*_db_*_[JOA]*.tif`
# do
#     echo ${image}
#     outfile=`basename ${image} .tif`_masked_${GHSMIN}.tif
#     gdal_calc.py -A ${image} -B ${mask} \
#                  --calc="A*B" \
#                  --NoDataValue=-9999 \
#                  --type=Float32 \
#                  --overwrite \
#                  --co COMPRESS=DEFLATE \
#                  --co PREDICTOR=3 \
#                  --outfile=${outfile}
# done
