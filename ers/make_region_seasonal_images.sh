#!/bin/bash

# make seasonal mean dB geotiffs
region="$1"

if [ "${region}" == "" ]
then
    echo "Must specify region."
    exit
fi

for year in `seq 1992 2000`
do
    for season in JFM AMJ JAS OND
    do
        echo "making seasonal mean and std for ${region} ${year} ${season}"
        ./make_seasonal_images.py -v -q ${season} ${region} ${year}
    done
done
