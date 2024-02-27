### AUXILIARY DATASETS
dirname(rstudioapi::getActiveDocumentContext()$path) %>% dirname() %>% setwd()
# Auxiliary objects 

months = c(1:12) %>% as.character() %>% str_pad(2, pad = "0")

# Import GADM Data
st_layers("Data_Sources/boundaries/gadm_410-levels.gpkg") #explore layer names
gadm0 <- st_read("Data_Sources/boundaries/gadm_410-levels.gpkg",
                 layer = "ADM_0")
gadm1 <- st_read("Data_Sources/boundaries/gadm_410-levels.gpkg",
                 layer = "ADM_1")
gadm0_poly = subset(as_tibble(gadm0[,c("GID_0")]), select = -c(geom))
gadm1_poly = subset(as_tibble(gadm1[,c("GID_1")]), select = -c(geom))

# Import raster of population density in 2000, 2005, 2010, 2015 | Resolution: 0.5
pop502000 = raster('Data_Sources/weights/pop502000density.asc') #ascii file of pop density
pop502000[is.na(pop502000[])] <- 0
crs(pop502000) = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs+ towgs84=0,0,0"

pop502005 = raster('Data_Sources/weights/pop502005density.asc') #ascii file of pop density
pop502005[is.na(pop502005[])] <- 0
crs(pop502005) = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs+ towgs84=0,0,0"

pop502010 = raster('Data_Sources/weights/pop502010density.asc') #ascii file of pop density
pop502010[is.na(pop502010[])] <- 0
crs(pop502010) = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs+ towgs84=0,0,0"

pop502015 = raster('Data_Sources/weights/pop502015density.asc') #ascii file of pop density
pop502015[is.na(pop502015[])] <- 0
crs(pop502015) = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs+ towgs84=0,0,0"

# Import raster of population density in 2000, 2005, 2010, 2015 | Resolution: 0.25
pop252000 = raster('Data_Sources/weights/pop252000density.asc') #ascii file of pop density
pop252000[is.na(pop252000[])] <- 0
crs(pop252000) = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs+ towgs84=0,0,0"

pop252005 = raster('Data_Sources/weights/pop252005density.asc') #ascii file of pop density
pop252005[is.na(pop252005[])] <- 0
crs(pop252005) = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs+ towgs84=0,0,0"

pop252010 = raster('Data_Sources/weights/pop252010density.asc') #ascii file of pop density
pop252010[is.na(pop252010[])] <- 0
crs(pop252010) = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs+ towgs84=0,0,0"

pop252015 = raster('Data_Sources/weights/pop252015density.asc') #ascii file of pop density
pop252015[is.na(pop252015[])] <- 0
crs(pop252015) = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs+ towgs84=0,0,0"

resligh = c(0.008333333, 0.008333333)
lightext = c(-180,180,-65,75)

matzer1 = rep(0, 60*1440)
matzer2 = rep(0, 100*1440)

# Block for lights at year 2000
lights2000 =raster("Data_Sources/weights/lights2000.tif")
lights252000 = lights2000 %>% aggregate(fact = 30, quick=FALSE, expand=FALSE)
crs(lights252000) = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs+ towgs84=0,0,0"
lights252000 = lights252000 %>% setExtent(lightext, keepres=TRUE)
newval = c(matzer1, values(lights252000), matzer2)
lights252000 = lights252000 %>% setExtent( c(-180,180,-90,90), keepres=TRUE)
lights252000 = setValues(lights252000, newval)
lights252000[is.na(lights252000[])] <- 0
lights502000 = aggregate(lights252000, fact = 2)


# Block for lights at year 2005
lights2005 =raster("Data_Sources/weights/lights2005.tif")
lights252005 = lights2005 %>% aggregate(fact = 30, quick=FALSE, expand=FALSE)
crs(lights252005) = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs+ towgs84=0,0,0"
lights252005 = lights252005 %>% setExtent(lightext, keepres=TRUE)
newval = c(matzer1, values(lights252005), matzer2)
lights252005 = lights252005 %>% setExtent( c(-180,180,-90,90), keepres=TRUE)
lights252005 = setValues(lights252005, newval)
lights252005[is.na(lights252005[])] <- 0
lights502005 = aggregate(lights252005, fact = 2)

# Block for lights at year 2010
lights2010 =raster("Data_Sources/weights/lights2010.tif")
lights252010 = lights2010 %>% aggregate(fact = 30, quick=FALSE, expand=FALSE)
crs(lights252010) = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs+ towgs84=0,0,0"
lights252010 = lights252010 %>% setExtent(lightext, keepres=TRUE)
newval = c(matzer1, values(lights252010), matzer2)
lights252010 = lights252010 %>% setExtent(c(-180,180,-90,90), keepres=TRUE)
lights252010 = setValues(lights252010, newval)
lights252010[is.na(lights252010[])] <- 0
lights502010 = aggregate(lights252010, fact = 2)


# Block for lights at year 2015
lights2015 =raster("Data_Sources/weights/lights2015.tif") 
lights252015 = lights2015 %>% aggregate(fact = 30, quick=FALSE, expand=FALSE)
crs(lights252015) = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs+ towgs84=0,0,0"
lights252015 = lights252015 %>% setExtent(lightext, keepres=TRUE)
newval = c(matzer1, values(lights252015), matzer2)
lights252015 = lights252015 %>% setExtent( c(-180,180,-90,90), keepres=TRUE)
lights252015 = setValues(lights252015, newval)
lights252010[is.na(lights252010[])] <- 0

ll = length(values(lights252015))

# Solve the issue with the auroras - year 2015
val45N = values(lights252000)[1:(360*4*4*45)]*values(lights252005)[1:(360*4*4*45)]*values(lights252010)[1:(360*4*4*45)]
val45S = values(lights252000)[(ll-360*4*4*45+1):ll]*values(lights252005)[(ll-360*4*4*45+1):ll]*values(lights252010)[(ll-360*4*4*45+1):ll]
values(lights252015)[1:(360*4*4*45)] = values(lights252015)[1:(360*4*4*45)]*(val45N!=0)
values(lights252015)[(ll-360*4*4*45+1):ll] = values(lights252015)[(ll-360*4*4*45+1):ll]*(val45S!=0)
lights502015 = aggregate(lights252015, fact = 2)

# .........................................
# CropLand data
# -------------------------
# Note: we multiply by the ratio of the total grid area over the total land area. 
# --> our subsequent weighting detects gets the portion of the country / region inside a certain grid.
# If this portion borders only with the sea / ocean, we would underestimate the amount of land area (note: the 
# land area data are given as the area of arable and usable land).
# ........................
# Import the total and land area files
totalA = raster("Data_Sources/weights/garea_cr.asc")
landA = raster("Data_Sources/weights/maxln_cr.asc")
totalA[is.na(totalA[])] <- 0
landA[is.na(landA[])] <- 0
totalA25 = totalA %>% aggregate(fact = 3, quick=FALSE, expand=FALSE, fun = sum) %>% setExtent( c(-180,180,-90,90), keepres=TRUE)
totalA50 = totalA25 %>% aggregate(fact = 2, quick=FALSE, expand=FALSE, fun = sum) %>% setExtent( c(-180,180,-90,90), keepres=TRUE)
landA25 = landA %>% aggregate(fact = 3, quick=FALSE, expand=FALSE, fun = sum) %>% setExtent( c(-180,180,-90,90), keepres=TRUE)
landA50 = landA25 %>% aggregate(fact = 2, quick=FALSE, expand=FALSE, fun = sum) %>% setExtent( c(-180,180,-90,90), keepres=TRUE)

for (y in seq(2000,2015, by = 5)){
  ychar = as.character(y)
  # import the cropland relative to a certain year
  cropl = raster(paste0("Data_Sources/weights/cropland", ychar, "AD.asc"))
  cropl[is.na(cropl[])] <- 0
  crs(cropl) = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs+ towgs84=0,0,0"
  # aggregate the raster values to have .25 and .50 degree grids
  cropl25 = cropl %>% aggregate(fact = 3, quick=FALSE, expand=FALSE, fun = sum) %>% setExtent( c(-180,180,-90,90), keepres=TRUE)
  cropl50 = cropl25 %>% aggregate(fact = 2, quick=FALSE, expand=FALSE, fun = sum) %>% setExtent( c(-180,180,-90,90), keepres=TRUE)
  cropl25 = cropl25 *  totalA25 / landA25
  cropl25[is.na(cropl25[])] <- 0
  cropl25[!is.finite(cropl25[])] <- 0
  cropl50 = cropl50 *  totalA50 / landA50
  cropl50[is.na(cropl50[])] <- 0
  cropl50[!is.finite(cropl50[])] <- 0
  # final assignment to create new object
  assign(
    paste0("cropl25", ychar), cropl25
  )
  assign(
    paste0("cropl50", ychar), cropl50
  )
  print(y)
}


# ---------------------------------------------------
# Population count data from HYDE 3.2 and GPW v4
# ..........................................
for (y in seq(1900,2020, by = 10)){
  ychar = as.character(y)
  # import the cropland relative to a certain year
  popc = raster(paste0("Data_Sources/weights/popc_", ychar, "AD.asc"))
  popc[is.na(popc[])] <- 0
  crs(popc) = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs+ towgs84=0,0,0"
  # aggregate the raster values to have .25 and .50 degree grids
  if (y != 2020){
    popc25 = popc %>% aggregate(fact = 3, quick=FALSE, expand=FALSE, fun = sum) %>% setExtent( c(-180,180,-90,90), keepres=TRUE)
  } else {
    popc25 = popc
  }
  popc50 = popc25 %>% aggregate(fact = 2, quick=FALSE, expand=FALSE, fun = sum) %>% setExtent( c(-180,180,-90,90), keepres=TRUE)
  popc25 = popc25 *  totalA25 / landA25
  popc25[is.na(popc25[])] <- 0
  popc25[!is.finite(popc25[])] <- 0
  popc50 = popc50 *  totalA50 / landA50
  popc50[is.na(popc50[])] <- 0
  popc50[!is.finite(popc50[])] <- 0
  # final assignment to create new object
  assign(
    paste0("popc25", ychar), popc25
  )
  assign(
    paste0("popc50", ychar), popc50
  )
  print(y)
}