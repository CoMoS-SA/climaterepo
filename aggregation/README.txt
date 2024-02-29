README for the Code and the links to the data sources to produce the aggregated climate time-series available from https://share.streamlit.io/app/weightedclimatedata/ and extensively discussed in the Data Article "A unified dataset for pre-processed climate indicators weighted by gridded economic activity"


#------------------------------------------------------

"aggregation"
- daily
	|-- get_era5_hourly.py ------> to retrieve the hourly data on temperature and precipitation from ERA5 
	|-- from_hourly_to_daily.py -> to aggregate the hourly grids and obtain daily values
	'-- era5.aggregate.R ---> to compute the daily temperature and precipitation time series for countries and regions

- AUXIL.R ---> to load the weights of the grids and the administrative boundaries
- CRU.R -----> to compute the climate data using the CRU data source (monthly)
- ERA5  -----> to compute the climate data using the ERA5 data source (monthly)
- SPEI ------> to compute the SPEI historical values using the CSIC data source (monthly)
- UDELA -----> to compute the climate data using the UDELA data source (monthly)

#-------------------------------------------

As regards the data sources we used

- boundaries
	'-- gadm_410-levels.gpkg --> contains the different administrative boundary levels. Retrieved from (https://gadm.org/)

- CRU
	|-- cru_ts4.07.1901.2022.pre.dat.nc --> NC file with CRU TS precipitation grids. Available from https://crudata.uea.ac.uk/cru/data/hrg/cru_ts_4.07/cruts.2304141047.v4.07/pre/
	'-- cru_ts4.07.1901.2022.tmp.dat.nc --> NC file with CRU TS temperature grids. Available from https://crudata.uea.ac.uk/cru/data/hrg/cru_ts_4.07/cruts.2304141047.v4.07/tmp/

- ERA
	|-- era5all.nc --> NC file with ERA5 precipitation and temperature grids. Retrievable from https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels-monthly-means?tab=form
	+ Product type: monthly averaged reanalysis;
	+ Variable: 2m temperature / Total precipitation / single levels;
	+ Format: NetCDF.
	'-- era5extent --> example file of an ERA5 NC object, useful for resampling other grid files to ERA5 grids system.

- SPEI
	'-- spei.nc --> NC file with SPEI grids from CSIC. Available from https://digital.csic.es/handle/10261/268088

- UDELA
	|-- PREC --> contains the precipitation files from UDELA --> https://psl.noaa.gov/data/gridded/data.UDel_AirT_Precip.html
	'-- TMP ---> contains the temperature files from UDELA ----> https://psl.noaa.gov/data/gridded/data.UDel_AirT_Precip.html

- weights
	|-- lights**YEAR**.tif ----------> original night-light grids. Available from:		 https://figshare.com/articles/dataset/Harmonization_of_DMSP_and_VIIRS_nighttime_light_data_from_1992-2018_at_the_global_scale/9828827/2
	|-- lights[25_50]**YEAR**.tif ---> night-light grids at a 0.25/0.5 degree resolution
	|-- pop[25_50]**YEAR**.asc ------> population density (population per km2 of land area) grids at a 0.25/0.5 degree resolution. Available from: https://sedac.ciesin.columbia.edu/data/set/gpw-v4-population-density-rev11
	|-- cropland**YEAR**AD.asc ------> Arable and Permanent Crop Land Area as defined by the UN. Available from HYDE 3.2:  https://easy.dans.knaw.nl/ui/datasets/id/easy-dataset:74467
	|-- cropland[25_50]**YEAR**.asc -> cropland grids at a 0.25/0.5 degree resolution.
	'-- popc**YEAR**AD.asc ----------> population count grids. From both HYDE 3.2 (until 2010) and GPW (for 2020).

#----------------------------------------------------------------
Laptop characteristics:
- Microsoft Windows 11 Pro
- x64 System
- Processor 11th Gen Inter(R) Core(TM) i7-1165G7 @ 2.80GHz, 2803 Mhz, 4 Core(s), 8 Logical Processors
- RAM 16GB

The Python operations to download the hourly data from ERA5 have been performed via a virtual machine.

# ------------------------------------------------------------------

The following libraries have been loaded for:
- R session. R version 4.2.1. || dataPreparation_1.1.1 / stringr_1.4.0 / rstudioapi_0.14 / arrow_13.0.0  / dplyr_1.1.3 / lubridate_1.8.0 / sf_1.0-8 / terra_1.6-7          
 / raster_3.5-29 / sp_1.5-0 / exactextractr_0.9.1  
- Python session. Python version 3.9.11 || cdsapi 0.6.1 / pandas 2.1.0 / xarray 2024.2.0
