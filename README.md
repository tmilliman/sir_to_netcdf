# sir_to_netcdf

This collection of python and bash scripts was used to create NetCDF
files for for the dataset available at
[http://www.ciesin.columbia.edu/data/seasonal-urban-backscatter/](http://www.ciesin.columbia.edu/data/seasonal-urban-backscatter/)
A description of this dataset has been submitted to Scientific Data
for publication in August 2021:

## Overview

These scripts make use of scatterometer image data obtained from the
[Scatterometer Climate Record Pathfinder](https://www.scp.byu.edu/)
site (SCP) at Brigham Young University (BYU). These scripts were part
of an effort to collect the data from that site and reorganize and
format it into a form that is useful for studying decadal scale
changes in urban development.

## Usage

These scripts were developed on unix-like systems (Mac OS X and Debian
Linux).  No effort has been made to ensure the scripts run unmodified
in other environments.  The `python3` and `bash` code is hopefully
mostly portable.  In some of the bash scripts other common unix utilities
like `awk` or `ncftpget` are used which may need to be installed for
the scripts to work as is.

### Getting the Scripts

The scripts in this repository can be downloaded as a single
[zipfile](https://github.com/tmilliman/urban_backscatter/archive/refs/heads/main.zip).
Alternatively, using git you can clone the repository:

    git clone https://github.com/tmilliman/sir_to_netcdf.git

### Setting up a Virtual Environment

The [`miniconda`](https://docs.conda.io/en/latest/miniconda.html)
package manager was used to set up a virtual environment for running
the scripts.  You can set up a virtual environment, `urban_backscatter`,
by doing the following:

    conda env create --file environment.yml
    conda activate sirpy
    python -m pip install git+https://github.com/tmilliman/sirpy2.git

### Outline of Steps

The conversion process involves many steps that are repeated for
each of the three instruments in the respecitve directories (ers,
qscatv2, ascat).

In each instrument directory and for each of the 14 SCP regions:

1. use `get_byu_data.sh` to download .sir image files from `ftp.scp.byu.edu`
2. use `make_region_geotiffs.sh` to covert .sir images files to geotiff format
3. use `make_region_seasonal_images.sh` to create images of seasonal means and
   standard deviations

In the geotiff_mosaics sub-directory for each of the 14 SCP regions

4. use `make_seasonal_4326_images.sh` to reproject the seasonal geotiff images

Then mosaic the regional images and apply an urban mask

5. use `mosaic_seasonal_images.sh` to mosaic the seasonal regional images
6. use `apply_masks.sh` to apply urban and water mask to seasonal images

Finally, create the netcdf files.  Separate the mean and standard deviations
just to keep file sizes smaller

7. use `create_masked_seasonal_mean_netcdf.py` to create seasonal mean netcdf
8. use `create_masked_seasonal_std_netcdf.py` to create seasonal std netcdf
9. use `create_seasonal_mean_netcdf.py` to create masked seasonal mean netcdf
10. use `create_seasonal_std_netcdf.py` to create masked seasonal std netcdf

### Notes

When creating the seasonal netcdf files full years are
constructed even if there is no data for a season.  In this case an
empty (all NODATA) image is used for the missing geotiff file.  For
example, for QuikSCAT the first images in 1999 were for July.  So there
was no JFM or AMJ image.

    cp qscat_missing_data_image.tif qscat_quev_mean_db_1999_JFM.tif
    cp qscat_missing_data_image.tif qscat_quev_std_db_1999_JFM.tif
    cp qscat_missing_data_image.tif qscat_quev_mean_db_1999_AMJ.tif
    cp qscat_missing_data_image.tif qscat_quev_std_db_1999_AMJ.tif
    cp qscat_missing_data_image.tif qscat_quev_mean_db_1999_JFM_masked_20.tif
    cp qscat_missing_data_image.tif qscat_quev_std_db_1999_JFM_masked_20.tif
    cp qscat_missing_data_image.tif qscat_quev_mean_db_1999_AMJ_masked_20.tif
    cp qscat_missing_data_image.tif qscat_quev_std_db_1999_AMJ_masked_20.tif


## Citation

Frolking, Steve, Tom Milliman, Richa Mahtta, Aaron Paget, David G. Long,
Karen C. Seto. 2021. **A global urban backscatter time series data (ERS,
QuikSCAT, ASCAT) set for 1993-2020**,
v1 (Preliminary Release). Palisades, NY: NASA Socioeconomic Data and
Applications Center (SEDAC). DOI: To be assigned following peer review.
Accessed DAY MONTH YEAR.
