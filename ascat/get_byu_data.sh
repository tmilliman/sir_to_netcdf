#!/bin/bash

# script to pull ascat data from ftp.scp.byu.edu 

region=$1
if [ "${region}" = "" ]
then
    echo "Must specify region!"
    exit 1
fi
product=msfa

for year in `seq 2007 2020`
do
    scriptfile=get_${region}_${year}.sh
    echo creating ${scriptfile}
    ./get_byu_data.py ${region} ${product} ${year} > ./${scriptfile}
    echo running ${scriptfile}
    bash ./${scriptfile}
    rm ${scriptfile}
done
