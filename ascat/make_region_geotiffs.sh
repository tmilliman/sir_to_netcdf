#!/bin/bash

# script to make geotiffs from ascat images
region="$1"

if [ "${region}" == "" ]
then
    echo "Must specify region."
    exit
fi


for file in `find [12]* -type f -name \*\*msfa-a-${region}\*\.sir\.gz`
do
    echo ${file}
    gunzip -v ${file}
    dirname=`dirname ${file}`
    sirname=`basename ${file} .gz`
    tiffname=`basename ${sirname} .sir`.tif
    year=`echo ${dirname} | awk -F\/ '{print $2}'`
    sir2geotiff ${dirname}/${sirname}
    gzip -v ${dirname}/${sirname}
done
