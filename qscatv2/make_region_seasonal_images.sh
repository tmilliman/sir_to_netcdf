#!/bin/bash

# make seasonal mean dB geotiffs
region="$1"

if [ "${region}" == "" ]
then
    echo "Must specify region."
    exit
fi

for year in `seq 1999 2009`
do
    for season in JAS OND JFM AMJ
    do
        echo "making seasonal mean and std for ${region} ${year} ${season}"
        ./make_seasonal_images.py -v -q ${season} ${region} ${year}
    done
done
