#!/bin/bash

# script to pull ERS1/2 data from BYU
region=$1
if [ "${region}" = "" ]
then
    echo "Must specify region!"
    exit 1
fi

product=ers1

for year in `seq 1993 1996`
do
    scriptfile=get_${region}_${year}.sh
    echo creating ${scriptfile}
    ./get_byu_data.py ${region} ${product} ${year} > ./${scriptfile}
    echo running ${scriptfile}
    bash ./${scriptfile}
    rm ${scriptfile}
done

product=ers2

for year in `seq 1996 2001`
do
    scriptfile=get_${region}_${year}.sh
    echo creating ${scriptfile}
    ./get_byu_data.py ${region} ${product} ${year} > ./${scriptfile}
    echo running ${scriptfile}
    bash ./${scriptfile}
    rm ${scriptfile}
done
