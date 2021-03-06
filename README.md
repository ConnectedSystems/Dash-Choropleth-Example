# Dash Choropleth Example

Example choropleth map with Dash.

Requested by eddy_oj at https://community.plot.ly/t/create-your-own-choropleth-map-with-custom-shapefiles/2567/18

## Environment Setup

[(Ana/Mini)conda](https://conda.io/docs/user-guide/install/download.html) is used to manage my different project environments.

The same (conda) environment used to develop this example can be created using

**Windows:**

`conda env create -n choro-example -f win_environment.yml`

**\*nix platforms**

`conda env create -n choro-example -f nix_environment.yml`

This will install all necessary python packages for the example. Thanks to [Steve98654](https://github.com/steve98654) for providing the \*nix environment file.

Inspect the `[win\nix]_environment.yml` file for the list of packages used.
These can be manually installed (e.g. via `pip`) if the use of `conda` is undesirable.

Once finished, the environment may be removed:

`conda env remove -n choro-example`

## Running

Activate the conda environment:

`activate choro-example` on Windows.

`source activate choro-example` on \*nix

Edit `choropleth_example.py` and specify your mapbox key.

Then run: `python choropleth_example.py`

Open web browser to http://127.0.0.1:8051/

## Other Notes:

Example using data on Limited English Proficiency in Portland.

Shapefile sourced from:

https://gis-pdx.opendata.arcgis.com/datasets/a0e5ed95749d4181abfb2a7a2c98d7ef_121


~~Note that there is currently a bug in dash which breaks interactions after second layer change.~~
[Fixed 10 July 2018](https://github.com/plotly/dash-core-components/pull/228)
See https://github.com/plotly/dash/issues/223 for more info.
