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

### Setting up a Virtual Environment

The [`miniconda`](https://docs.conda.io/en/latest/miniconda.html)
package manager was used to set up a virtual environment for running
the scripts.  You can set up a virtual environment, `urban_backscatter`,
by doing the following:

    conda env create --file environment.yml
    conda activate sirpy
    python -m pip install git+https://github.com/tmilliman/sirpy2.git




## Citation

Frolking, Steve, Tom Milliman, Richa Mahtta, Aaron Paget, David G. Long,
Karen C. Seto. 2021. **A global urban backscatter time series data (ERS,
QuikSCAT, ASCAT) set for 1993-2020**,
v1 (Preliminary Release). Palisades, NY: NASA Socioeconomic Data and
Applications Center (SEDAC). DOI: To be assigned following peer review.
Accessed DAY MONTH YEAR.

