#!/bin/bash

# script to submit jobsd to create all the netcdf files
ts ./create_monthly_mean_netcdf.py
ts ./create_monthly_std_netcdf.py
ts ./create_masked_seasonal_mean_netcdf.py
ts ./create_masked_seasonal_std_netcdf.py
ts ./create_seasonal_mean_netcdf.py
ts ./create_seasonal_std_netcdf.py
