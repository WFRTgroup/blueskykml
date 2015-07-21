# blueskykml

This package was build using code extracted from the kml3 module in BlueSky
Framework.

## Non-python Dependencies

Whether cloning the repo or installing with pip, you'll first need to
manually install netcdf and gdal libraries, which blueskykml depends on.

On a mac, you can do so with [Homebrew](http://brew.sh/):

    brew install homebrew/science/netcdf
    brew install gdal --with-netcdf --enable-unsupported

Note that the '--with-netcdf' option is required to build gdal with the
netCDF driver. See http://trac.osgeo.org/gdal/wiki/NetCDF for more information.

On ubuntu, the following should be sufficient:

    sudo apt-get install libnetcdf-dev
    sudo apt-get install python-gdal
    sudo apt-get install libgdal1-1.7.0

## Development

### Clone Repo

Via ssh:

    git clone git@github.com:pnwairfire/blueskykml.git

or http:

    git clone https://github.com/pnwairfire/blueskykml.git

### Install Dependencies@

After installing the non-python dependencies (mentioned above), run the
following to install required python packages:

    pip install -r requirements.txt

### Setup Environment

To import blueskykml in development, you'll have to add the repo root
directory to the search path.

## Installing

First install the non-python dependencies (mentioned above).

### Installing With pip

Install pip, if it isn't yet installed:

    sudo apt-get install python-pip

Then, to install, for example, v0.2.1, use the following:

    sudo pip install --trusted-host pypi.smoke.airfire.org -i http://pypi.smoke.airfire.org/simple blueskykml==0.2.1

If you get an error like    ```AttributeError: 'NoneType' object has no attribute 'skip_requirements_regex```, it means you need in upgrade pip.  One way to do so is with the following:

    pip install --upgrade pip

If, when you run makedispersionkml, you get the following error:

    *** Error: No module named _gdal_array

it's because your osgeo package (/path/to/site-packages/osgeo/) is
missing _gdal_array.so.  This happens when gdal is built on a
machine that lacks numpy.  To fix this, uninstall the gdal package
just installed, and then re-install with the --no-binary option to pip:

    pip uninstall -y GDAL
    pip install --no-binary :all: gdal==1.11.2

If this doesn't work, uninstall gdal, and then install it manually:

    pip uninstall -y GDAL
    wget https://pypi.python.org/packages/source/G/GDAL/GDAL-1.11.2.tar.gz
    tar xzf GDAL-1.11.2.tar.gz
    cd GDAL-1.11.2
    python setup.py install

### Installing With setup.py

To install blueskykml from the source repo, you can use the following:

    python ./setup.py install

## Using

Example uses:

    $ ./bin/makedispersionkml -c ./sample-config/makedispersionkml.ini \
        -o /path/to/bluesky/output/ -v -k ./smoke-dispersion.kmz -f fires.kmz

## Distributing

To build a distribution tarball, use the following.

    python ./setup.py sdist

This will create a tarball in ```REPO_ROOT/dist/```
