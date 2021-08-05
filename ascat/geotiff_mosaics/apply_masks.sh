#!/bin/bash

# test applying ghsl > 20 mask

GHSMIN=20
WFMAX=50
mask="mask_GHS${GHSMIN}_WF${WFMAX}.tif"

for image in `ls ascat_msfa_*_[JOA]*.tif | grep -v masked`
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

# for image in `ls ascat_msfa_*_[JOA]*.tif | grep -v masked`
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
