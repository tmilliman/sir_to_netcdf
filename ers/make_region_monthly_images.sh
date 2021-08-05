#!/bin/bash

# make monthly mean dB geotiffs
region="$1"

if [ "${region}" == "" ]
then
    echo "Must specify region."
    exit
fi

for year in `seq 1992 2000`
do
    monthlist=`seq 1 12`
    for month in ${monthlist}
    do
        echo "making monthly mean and std for ${region} ${year} ${month}"        
        ./make_monthly_images.py ${region} ${year} ${month}
    done
done
