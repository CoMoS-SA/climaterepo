##########################
# This script retrieves the hourly temperature and precipitation data from ERA5
# by using their API
########################## 


import cdsapi
import os
import glob

years =  [str(y) for y in range(1940,2024)]
  
# Retrieve all months for a given year.
months = ['01','02', '03','04', '05', '06','07', '08', '09', '10','11', '12']

c = cdsapi.Client()
vars = ['2m_temperature', 'total_precipitation']

year_month = []
for i in range(len(years)):
    for j in range(len(months)):
        new_pair = (years[i], months[j])
        year_month.append(new_pair)

for v in vars:
    for yrm in year_month[0:len(year_month)]:
        yr = yrm[0]
        mn = yrm[1]
        file_name = "download_" + "hourly" + "_" + v + "_" + yr + "_" + mn + ".nc"
        c.retrieve(
            'reanalysis-era5-single-levels',
            {
                'product_type': 'reanalysis',
                'format': 'netcdf',
                'variable': v,
                'year': [
                    yr
                ],
                'month': [
                    mn
                ],
                'day': [
                    '01', '02', '03',
                    '04', '05', '06',
                    '07', '08', '09',
                    '10', '11', '12',
                    '13', '14', '15',
                    '16', '17', '18',
                    '19', '20', '21',
                    '22', '23', '24',
                    '25', '26', '27',
                    '28', '29', '30',
                    '31',
                ],
                'time': [
                    '00:00', '01:00', '02:00',
                    '03:00', '04:00', '05:00',
                    '06:00', '07:00', '08:00',
                    '09:00', '10:00', '11:00',
                    '12:00', '13:00', '14:00',
                    '15:00', '16:00', '17:00',
                    '18:00', '19:00', '20:00',
                    '21:00', '22:00', '23:00',
                ],
                'area': [
                90, -180, -90,
                180,
            ]
            },
        file_name)
    
    
    
    



