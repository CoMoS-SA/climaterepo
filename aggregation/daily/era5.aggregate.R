library(dplyr)
library(exactextractr)
library(raster)
library(sf)
library(lubridate)
library(terra)
library(arrow)
library(data.table)
library(dataPreparation)
library(data.table)

# Set directory 
dirname(rstudioapi::getActiveDocumentContext()$path) %>% dirname() %>% dirname() %>% setwd()
rm(list=ls())

# Load the GADM0
gadm0 <- st_read("Data_Sources/boundaries/gadm_410-levels.gpkg",
                 layer = "ADM_0")
gadm1 <- st_read("Data_Sources/boundaries/gadm_410-levels.gpkg",
                 layer = "ADM_1")

gadm0_poly = subset(as_tibble(gadm0[,c("GID_0")]), select = -c(geom))
gadm1_poly = subset(as_tibble(gadm1[,c("GID_1")]),select = -c(geom))

# Import raster of population density in 2000, 2005, 2010, 2015 | Resolution: 0.25
pop252015 = raster('Data_Sources/weights/pop252015density.asc') # ascii file of pop density
pop252015[is.na(pop252015[])] <- 0
crs(pop252015) = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs+ towgs84=0,0,0"

# Import raster of lights
lights252015 = raster('Data_Sources/weights/lights252015.tif') # ascii file of lights density
lights252015[is.na(lights252015[])] <- 0
crs(lights252015) = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs+ towgs84=0,0,0"

# Import raster of cropland
cropl252015 = raster('Data_Sources/weights/cropland252015.asc')
cropl252015[is.na(cropl252015[])] <- 0
crs(cropl252015) = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs+ towgs84=0,0,0"

# Import raster of concurrent population
for (y in 194:202){
  ychar = paste0(as.character(y), "0")
  ras = raster(paste0('Data_Sources/weights/popc25', ychar, '.asc'))
  ras[is.na(ras[])] <- 0
  crs(ras) = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs+ towgs84=0,0,0"
  assign(
    paste0("popc", "25", ychar),
    ras
  )
}

# ...................
varshort = c("tmp", "pre")

funERAgadm <-  function(w, weight = weight, res = NULL, path, files, modal = NULL){
  out = tryCatch({
    
    file = paste0(path, "\\", files[w])
    
    if (modal == "concurrent"){
      # Extracting the first four-digit number using regular expression
      ychar <- regmatches(file, regexpr("\\d{4}", file))
      ychar = substr(ychar, 1, 3)
      weight = get(paste0("popc25", ychar, "0"))
      weight = resample(weight, ERA5extent, method='bilinear')
    }
    
    # Import ERA5 raster
    ERA5 = brick(file, level = 1)
    
    if (extent(ERA5)[1] > -1){
      ERA5 = rotate(ERA5)
    }
    crs(ERA5) = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs+ towgs84=0,0,0"
    
    if (modal %in% c("cropland", "concurrent")){
      country_ERA5 = exactextractr::exact_extract(ERA5, get(res), fun = "weighted_mean", weights = weight, progress = F)
      print(w)
    } else {
      country_ERA5 = exactextractr::exact_extract(ERA5, get(res), fun = "weighted_mean", weights = weight*area(ERA5), progress = F)
    }
    
    
    new_cols = gsub("weighted_mean.", "", colnames(country_ERA5))
    new_cols = gsub("\\.", "",new_cols)
    colnames(country_ERA5) = new_cols
    
    if (grepl("temperature", file)){
      country_ERA5 = country_ERA5 - 273.15 # Transform to Celsius
    } 
    country_ERA5 = fast_round(country_ERA5,digits = 2)
    write.csv(file,paste0("Code/daily/output/", m, as.character(w), ".csv"))
    country_ERA5},
    error = function(cond){
      write.csv("Error",paste0("Code/daily/output/","error_at_", m, as.character(w), ".csv"))
    })
  return(out)
}

mods = c("un", "lights", "pop", "cropland", "concurrent")
ress = c("gadm0", "gadm1")

ERA5extent = brick("Data_Sources/ERA5/era5extent.nc")

for (v in varshort){
  path = paste0("./daily.", v)
  files = path %>% list.files(pattern = ".nc")
  for (m in mods){
    # Resample the pop raster to make it consistent with ERA5
    if (m == "pop"){
      weight <- resample(pop252015, ERA5extent, method='bilinear')
      y = "2015"
    }
    if (m == "un"){
      weight = 1
      y = ""
    }
    if (m == "lights"){
      weight = resample(lights252015, ERA5extent, method='bilinear')
      y = "2015"
    }
    
    if (m == "cropland"){
      weight = resample(cropl252015, ERA5extent, method='bilinear')
      y = "2015"
    }
    
    if (m == "concurrent"){
      weight = "tbd"
      y = ""
    }
    
    for (r in ress){
      print(m)
      print(r)
      print(v)
      print("------------------")
      
      
      list <- lapply(c(1:length(files)), funERAgadm, weight = weight, res = r, files = files, path = path,
                     modal = m)
      list2 = do.call(cbind, list) %>% setDT()
      
      if (r == "gadm0"){
        list3 = cbind(gadm0_poly, list2)
        
      } else {
        list3 = cbind(gadm1_poly, list2)
      }
      
      tranp.names = list3[[1]]
      list3 = t(list3[,-1])%>% data.frame()
      colnames(list3) = tranp.names
      Date = row.names(list3)
      list3 = cbind(Date, list3)
      colnames(list3) = gsub("\\.", "_", colnames(list3))
      
      savename = paste(
        r,
        "era",
        v,
        m,
        y,
        "daily.parquet",
        sep = "_")
      
      write_parquet(list3, 
                    savename          
      )
    }
  }
}

