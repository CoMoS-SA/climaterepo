library(sf)
library(dplyr)
library(exactextractr)
library(lubridate)
library(raster)
library(terra)
library(rstudioapi)


dirname(rstudioapi::getActiveDocumentContext()$path) %>% setwd()

# Load SHAPE Countries
bke_cntry = st_read(paste0(getwd(),"/shape/country.shp"))

# Load DENS
bke_pop = raster('bke_pop.asc') #ascii file delle densità

# Matrices with zero to fill up
matzer1 = rep(0, 10*720)
matzer2 = rep(0, 64*720)
newval = c(matzer1, values(bke_pop), matzer2)
bke_pop = bke_pop %>% setExtent( c(-180,180,-90,90), keepres=TRUE)
bke_pop = setValues(bke_pop, newval)
bke_pop[is.na(bke_pop[])] <- 0
crs(bke_pop) = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs+ towgs84=0,0,0"

#########################
# Untar the prec and temperature
library(utils)

# PRECIPITATION
# Read the first year

precUdel = read.table(paste0(getwd(), "/Global2011Pv301.tar", '/precip.1900'), sep = "" , header = F ,
                      na.strings ="", stringsAsFactors= F)[1:14]
colonne = c('long', 'lat', 'jan1900', 'feb1900', 'mar1900', 'apr1900','may1900', 'jun1900', 'jul1900', 'aug1900', 'sep1900', 'oct1900', 'nov1900', 'dec1900')
colnames(precUdel) <-  colonne


for (i in 1901:2010){
  temp = read.table(paste0(getwd(), '/Global2011Pv301/precip.', as.character(i)), sep = "" , header = F ,
                    na.strings ="", stringsAsFactors= F)
  temp = temp[, 3:(length(temp))] # not read the lat and long
  colnames(temp) = paste0(month.abb %>% tolower(), as.character(i))
  precUdel = cbind(precUdel, temp) # create unique dataset. Row: latlon point in the Earth. Column: total precipitation in the pair month-year

  compl_row <- list(long=179.75, lat=89.75)
  precUdel2 = precUdel
  precUdel2[nrow(precUdel2) + 1, names(compl_row)] <- compl_row
} 

rasterone_prec <- rasterFromXYZ(precUdel2)

crs(rasterone_prec) = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs+ towgs84=0,0,0"

##########################

# TEMPERATURE
# Read the first year

tmpUdel = read.table(paste0(getwd(), '/Global2011Tv301/air_temp.1900'), sep = "" , header = F ,
                      na.strings ="", stringsAsFactors= F)[1:14]
colonne = c('long', 'lat', 'jan1900', 'feb1900', 'mar1900', 'apr1900','may1900', 'jun1900', 'jul1900', 'aug1900', 'sep1900', 'oct1900', 'nov1900', 'dec1900')
colnames(tmpUdel) <-  colonne



for (i in 1901:2010){
  temp = read.table(paste0(getwd(), '/Global2011Tv301.tar/air_temp.', as.character(i)), sep = "" , header = F ,
                    na.strings ="", stringsAsFactors= F)
  temp = temp[, 3:(length(temp))] #not read the lat and long
  colnames(temp) = paste0(month.abb %>% tolower(), as.character(i))
  tmpUdel = cbind(tmpUdel, temp) #create unique dataset. Row: latlon point in the Earth. Column: mean temperature in pair month-year
  
  compl_row <- list(long=179.75, lat=89.75)
  tmpUdel2 = tmpUdel
  tmpUdel2[nrow(tmpUdel2) + 1, names(compl_row)] <- compl_row
} 

rasterone_tmp <- rasterFromXYZ(tmpUdel2)

crs(rasterone_tmp) = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs+ towgs84=0,0,0"

########################


# Compute the precipitation
months = month.abb %>% tolower()
isopoly = bke_cntry %>% dplyr::select(GMI_CNTRY, POP_CNTRY, geometry) 
isopoly2 = subset(as_tibble(isopoly[,c("GMI_CNTRY", "POP_CNTRY")]),select = -c(geometry)) %>%
  distinct()

library(stats)

country_pre_dela = exact_extract(rasterone_prec, isopoly, 
                  fun = 'weighted_mean', weights = area(bke_pop)*bke_pop)

isopoly = bke_cntry %>% dplyr::select(GMI_CNTRY, POP_CNTRY, geometry) %>% as_tibble() %>% dplyr::select(-c(geometry))

country_pre_dela2 = cbind(isopoly, country_pre_dela)
count = 3
for (i in 1900:2010){
  colnames(country_pre_dela2)[c(count:(count+11))] = paste0(months, as.character(i))
  count = count +12
} 

burkenspre = country_pre_dela2[,1:2] %>% data.frame()
colnames(burkenspre)[1] <- "iso"
colnames(burkenspre)[2] <- "pop"
count = 3
ncol = 3
for (i in 1900:2010){
  sub = country_pre_dela2[, count:(count+11)]
  burkenspre[,ncol] = rowSums(sub)
  colnames(burkenspre)[ncol] <- i
  count = count +12
  ncol = ncol +1
}

# Apply the custom aggregation function to the numerical columns to pick the most
# populated ISO country in case there are duplicate case

burkenspre.final <- burkenspre %>%
  group_by(iso) %>%
  filter(pop == max(pop)) %>%
  dplyr::select(-c(pop))

library(tidyr)
burkensprelong = gather(burkenspre.final, year, prens, "1900":"2010") %>%
  na.omit() %>% filter(year>= 1960 & year<=2010)

#-------------------------------------------------------
### Temperature
months = c('jan', 'feb', 'mar', 'apr','may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec')
isopoly = bke_cntry %>% dplyr::select(GMI_CNTRY, geometry) 
isopoly2 = subset(as_tibble(isopoly[,c("GMI_CNTRY")]),select = -c(geometry)) %>%
  distinct()
country_tmp_dela = exact_extract(rasterone_tmp, isopoly, 
                                 fun = 'weighted_mean', weights = area(bke_pop)*bke_pop)

isopoly = bke_cntry %>% dplyr::select(GMI_CNTRY, POP_CNTRY, geometry) %>% as_tibble() %>% dplyr::select(-c(geometry))

country_tmp_dela2 = cbind(isopoly, country_tmp_dela)
count = 3
for (i in 1900:2010){
  colnames(country_tmp_dela2)[c(count:(count+11))] = paste0(months, as.character(i))
  count = count +12
} 

burkenstmp = country_tmp_dela2[,1:2] %>% data.frame()
colnames(burkenstmp)[1] <- "iso"
colnames(burkenstmp)[2] <- "pop"
count = 3
ncol = 3
for (i in 1900:2010){
  sub = country_tmp_dela2[, count:(count+11)]
  burkenstmp[,ncol] = rowMeans(sub)
  colnames(burkenstmp)[ncol] <- i
  count = count +12
  ncol = ncol +1
}

# Apply the custom aggregation function to the numerical columns: in case of
# two iso countries with the same code, we pick the one with the bigger population

burkenstmp.final <- burkenstmp %>%
  group_by(iso) %>%
  filter(pop == max(pop)) %>%
  dplyr::select(-c(pop))

library(tidyr)
burkenslongtmp = gather(burkenstmp.final, year, tmpns, "1900":"2010") %>%
  na.omit() %>% filter(year>= 1960 & year<=2010)
burkens = merge(burkenslong,burkenslongtmp)

# Load Burke Data

burke = read.csv("burkeData.csv", header = TRUE, check.names = FALSE)
subvars <- c("iso", "year", "UDel_temp_popweight", "UDel_precip_popweight")
burke =  burke[,subvars]
burke = rename(burke, tmp = UDel_temp_popweight, pre = UDel_precip_popweight)
burkena = na.omit(burke)


# start the comparison
# check countries first
countryns = burkens$iso %>% unique()
countryna = burkena$iso %>% unique()
countryna[!countryna%in%countryns]

bkecmpr = merge(burkena, burkens, all.x = TRUE, by = c("iso", "year"))

##############################

