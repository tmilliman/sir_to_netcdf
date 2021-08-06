#!/bin/bash

# script to make geotiffs from ascat images
region=$1
if [ "${region}" = "" ]
then
    echo "Must specify region!"
    exit 1
fi

product='ers[12]'

for file in `find [12]* -type f -name \*\*${product}-[aV]-${region}\*\.sir\.gz`
do
    # avoid picking up the 1-day data files
    start_day=`basename ${file} .sir.gz | awk -F- '{print $4}'`
    end_day=`basename ${file} .sir.gz | awk -F- '{print $5}'`
    if [ ${end_day} = ${start_day} ]
    then
        continue
    fi

    echo ${file}
    dirname=`dirname ${file}`
    sirname=`basename ${file} .gz`
    tiffname=`basename ${sirname} .sir`.tif
    year=`echo ${dirname} | awk -F\/ '{print $2}'`
    gunzip -v -f ${file}
    sir2geotiff ${dirname}/${sirname}
    gzip -v -f ${dirname}/${sirname}
done
