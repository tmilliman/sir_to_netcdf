#!/bin/bash

# script to pull quikscat v2 data from BYU
region=$1
if [ "${region}" = "" ]
then
    echo "Must specify region!"
    exit 1
fi

product=quev

for year in `seq 1999 2009`
do
    scriptfile=get_${region}_${year}.sh
    echo creating ${scriptfile}
    ./get_byu_data.py ${region} ${product} ${year} > ./${scriptfile}
    echo running ${scriptfile}
    bash ./${scriptfile}
    rm ${scriptfile}
done
