#!/bin/bash

# make monthly mean power ratio geotiffs
region="$1"

if [ "${region}" == "" ]
then
    echo "Must specify region."
    exit
fi

for year in `seq 1999 2009`
do
    if [ ${year} = '1999' ]
    then
        monthlist=`seq 7 12`
    elif [ ${year} = '2009' ]
    then
        monthlist=`seq 1 11`
    else
        monthlist=`seq 1 12`
    fi
    for month in ${monthlist}
    do
        echo "making monthly mean and stdev for ${region} ${year} ${month}"
        ./make_monthly_db_images.py ${region} ${year} ${month}
    done
done
