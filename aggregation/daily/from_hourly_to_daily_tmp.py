##############################################
# This script starts from the hourly gridded files of temperatures and precipitation
# to produce the daily gridded files by taking the mean (in case of the temperatures)
# or by summing up the values (in case of the precipitation)
##############################################


import xarray as xr
import os 
import pandas as pd

os.chdir(r"/users/testa/Documents/Climate/hourly.tmp")

years = list(range(1940,2024)) 
months = ["01","02","03", "04", "05","06","07","08", "09","10","11","12"] 

filesAPI = []
for y in years:
    for m in months:
        filesAPI.append("download_hourly_2m_temperature_" + str(y) + "_" + m + ".nc")

for file in filesAPI:
    print(file)
    # Open the NetCDF file
    os.chdir(r"/users/testa/Documents/Climate/hourly.tmp")
    
    ds = xr.open_dataset(file)
    # Define the grouping factor
    grouping_factor = 24
    
    # Calculate the number of groups
    num_groups = ds.dims['time'] // grouping_factor
    
    # Create an empty dataset to store the grouped sums
    grouped_stat = []
    grouped_indexes = []
    
    # Perform grouping and summation
    for group_id in range(num_groups):
        start_idx = group_id * grouping_factor
        end_idx = (group_id + 1) * grouping_factor
        
        group_stat = ds.isel(time=slice(start_idx, end_idx)).mean(dim='time')
        
        # Add the group sum to the new dataset
        grouped_stat.append(group_stat)
        
        start_nc = ds.isel(time=slice(start_idx, start_idx+1)) 
        day = pd.to_datetime(start_nc.variables['time'].values[0]).strftime("X%Y.%m.%d")
        grouped_indexes.append(day)

    da_concat = xr.concat(grouped_stat, pd.Index(grouped_indexes, name='Day'))
    os.chdir(r"/users/testa/Documents/Climate/daily.tmp")
    new_file = file.replace("hourly", "daily")
    new_file = new_file[:14] + "_mean" +  new_file[14:]
    print("Writing data")
    da_concat.to_netcdf(new_file)
    print("----------------")
    ds.close()