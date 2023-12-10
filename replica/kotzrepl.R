library(sf)
library(dplyr)
library(reticulate)
library(exactextractr)
library(stringr)
library(lubridate)
library(rstudioapi)

dirname(rstudioapi::getActiveDocumentContext()$path) %>% dirname()%>% dirname() %>% setwd()

ERA5prec = brick("Data_Sources/ERA5/era5all.nc", var="tp", level = 1)
ERA5tmp = brick("Data_Sources/ERA5/era5all.nc", var="t2m", level = 1)
crs(ERA5prec) = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs+ towgs84=0,0,0"
crs(ERA5tmp) = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs+ towgs84=0,0,0"

gadm1 = st_read("Replica/Kotz/gadm36/gadm36_levels.gpkg", layer="level1")
gadm1_poly = subset(as_tibble(gadm1[,c("GID_0","NAME_1", "GID_1")]),select = -c(geom)) %>%
  distinct()

climvars = c("tmp", "pre")

dict_var = list(tmp = "t2m", pre = "tp")

months = c(1:12) %>% as.character() %>% str_pad(2, pad = "0")

dirname(rstudioapi::getActiveDocumentContext()$path) %>% dirname() %>% dirname() %>% setwd()

for (var in climvars){
  ERA5 = brick("Data_Sources/ERA5/era5all.nc", var= dict_var[[var]], level = 1)
  crs(ERA5) = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs+ towgs84=0,0,0"
  print(var)
  agg = exact_extract(ERA5, gadm1, fun = "weighted_mean", weights = area(ERA5))
        agg2 = agg[, c(1:(83*12))]
        agg2 = cbind(get(paste0(res, "_poly")), agg2)
        
        count = dict_count[[res]]
        for (i in 1940:2022){
          colnames(agg2)[c(count:(count+11))] = paste0(months, as.character(i))
          count = count +12
        }
        
        cols = names(agg2)
        for (i in 1:ncol(agg2)){
          if (startsWith(cols[i], "w")== TRUE){
            data_ch = str_sub(cols[i],-7,-1)
            data = as.Date(paste0(data_ch," 01"), format= "%b%Y %d")
            if (var == "pre"){
              agg2[,i] = agg2[,i]*days_in_month(data)*1000
            } else {
              agg2[,i] = agg2[,i]- 273.15
            }
            month = month(data)
            month =  str_sub(months[month],-3,-1)
            year = year(data)
            year = as.character(year)
            names(agg2)[i] <- paste0(month,year)
          }
        }
}


country_precERA_gadm1_un = exact_extract(ERA5prec, gadm1,  fun = 'weighted_mean', 
                                         weights = area(ERA5prec))

country_precERA2_gadm1_un = cbind(gadm1_poly, country_precERA_gadm1_un)
country_precERA2_gadm1_un = country_precERA2_gadm1_un[,c(1:3,472:951)]

months = c('wJan', 'wFeb', 'wMar', 'wApr','wMay', 'wJun', 'wJul', 'wAug', 'wSep', 'wOct', 'wNov', 'wDec')

count = 4
for (i in 1979:2018){
  colnames(country_precERA2_gadm1_un)[c(count:(count+11))] = paste0(months, as.character(i))
  count = count +12
} 

cols = names(country_precERA2_gadm1_un)
for (i in 1:ncol(country_precERA2_gadm1_un)){
  if (startsWith(cols[i], "w")== TRUE){
    data_ch = str_sub(cols[i],-7,-1)
    data = as.Date(paste0(data_ch," 01"), format= "%b%Y %d")
    country_precERA2_gadm1_un[,i] = country_precERA2_gadm1_un[,i]*days_in_month(data)*1000
    month = month(data)
    month =  str_sub(months[month],-3,-1)
    year = year(data)
    year = as.character(year)
    names(country_precERA2_gadm1_un)[i] <- paste0(month,year)
  }
}

cpea = country_precERA2_gadm1_un[,1:3]
count = 4
ncol = 4
for (i in 1979:2018){
  sub = country_precERA2_gadm1_un[, count:(count+11)]
  cpea[,ncol] = rowSums(sub)
  colnames(cpea)[ncol] <- i
  count = count +12
  ncol = ncol +1
}

# Set the directory where the files are located
dir <- paste0(getwd(), "/Replica/Katz/PT")

# Get a list of all files in the directory that begin with "data"
file_list <- list.files(path = dir, pattern = "^Pt_*")

# Loop through the list of files and import each one
data_kotz = data.frame()
for(file in file_list) {
  temp <- np$load(file)
  data_kotz <- data_kotz %>% rbind(temp)
}

kotz_compare <-  gather(cpea,"year","prec_NS",4:43)  
kotz_compare$prec_KOTZ = data_kotz %>% stack() %>% select(values) %>% rename(prec_KOTZ= values)


############################################
# Temperature
# ------------------------------------------

country_tmpERA_gadm1_un = exact_extract(ERA5tmp, gadm1,  fun = 'weighted_mean', 
                                         weights = area(ERA5tmp))


country_tmpERA2_gadm1_un = cbind(gadm1_poly, country_tmpERA_gadm1_un)
country_tmpERA2_gadm1_un = country_tmpERA2_gadm1_un[,c(1:3,472:951)]
months = c('wJan', 'wFeb', 'wMar', 'wApr','wMay', 'wJun', 'wJul', 'wAug', 'wSep', 'wOct', 'wNov', 'wDec')

count = 4
for (i in 1979:2018){
  colnames(country_tmpERA2_gadm1_un)[c(count:(count+11))] = paste0(months, as.character(i))
  count = count +12
} 

cols = names(country_tmpERA2_gadm1_un)
for (i in 1:ncol(country_tmpERA2_gadm1_un)){
  if (startsWith(cols[i], "w")== TRUE){
    data_ch = str_sub(cols[i],-7,-1)
    data = as.Date(paste0(data_ch," 01"), format= "%b%Y %d")
    country_tmpERA2_gadm1_un[,i] = country_tmpERA2_gadm1_un[,i]- 273.15
    month = month(data)
    month =  str_sub(months[month],-3,-1)
    year = year(data)
    year = as.character(year)
    names(country_tmpERA2_gadm1_un)[i] <- paste0(month,year)
  }
}

ctea = country_tmpERA2_gadm1_un[,1:3]
count = 4
ncol = 4
for (i in 1979:2018){
  sub = country_tmpERA2_gadm1_un[, count:(count+11)]
  ctea[,ncol] = rowMeans(sub)
  colnames(ctea)[ncol] <- i
  count = count +12
  ncol = ncol +1
}

# Set the directory where the files are located
dir <- paste0(getwd(), "/Replica/Katz/TMP")

# Get a list of all files in the directory that begin with "data"
file_list <- list.files(path = dir, pattern = "^T_*")

# Loop through the list of files and import each one
tmp_kotz = data.frame()
for(file in file_list) {
  temp <- np$load(file)
  temp <-  apply(temp[,1,,], c(1,2), mean)
  tmp_kotz <- tmp_kotz %>% rbind(temp)
}

kotz_compare$tmp_NS <-  ctea[4:43] %>% stack() %>% select(values) %>% rename(tmp_NS= values)
kotz_compare$tmp_KOTZ = tmp_kotz %>% stack() %>% select(values) %>% rename(tmp_KOTZ= values)

kotz_compare$tmp_NS = kotz_compare$tmp_NS %>% unlist() %>% as.numeric()
kotz_compare$tmp_KOTZ = kotz_compare$tmp_KOTZ %>% unlist()%>% as.numeric()
kotz_compare$prec_KOTZ = kotz_compare$prec_KOTZ %>% unlist()%>% as.numeric()

