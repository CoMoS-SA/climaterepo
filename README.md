# The Weighted Climate Data Repository Project

The Weighted Climate Data Repository Project aims at combining climate data from different sources in a single, accessible and organized repository. We offer three ways for accessing data:
- Dashboard access via [Web app](https://climaterepo.streamlitapp.com/)
- Script access via our scripts
- Direct access via GitHub (navigating through [this](https://github.com/testalorenzo/climate_repository) repository)

We let the user choose the preferred source of data. Currently, we offer data from [Climatic Research Unit (CRU TS)](https://www.uea.ac.uk/groups-and-centres/climatic-research-unit), [Delaware Climate Office](https://climate.udel.edu/), [ECMWF's ERA5](https://www.ecmwf.int/) and [CSIC](https://spei.csic.es/index.html). 

These are the variables, measured daily, monthly and annually, currently supported at both the [GADM](https://gadm.org/) spatial resolution of GADM0 and GADM1 administrative areas:
- Temperature
- Precipitation
- SPEI (Standardised Precipitation-Evapotranspiration Index)

Moreover, we also provide the possibility of weighting climate data by population density, night-time lights usage, cropland (measured in different years) and concurrent population count while linking grid data to administrative units. Data on population density have been retrieved from [GPWv4](https://sedac.ciesin.columbia.edu/data/set/gpw-v4-population-density-rev11); data on night lights usage have been retrieved from [Li et al. (2020)](https://www.nature.com/articles/s41597-020-0510-y); data on cropland and population count have been retrieved from [HYDE 3.2](https://archaeology.datastations.nl/dataset.xhtml?persistentId=doi:10.17026/dans-25g-gez3).

Finally, we also allow the user to specify a percentile or an absolute threshold value of the historic distribution of a geographic unit, counting for each month or year the number of days that are over the given threshold.

Stay tuned for updates!
