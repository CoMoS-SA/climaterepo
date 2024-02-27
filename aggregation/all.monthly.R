library(exactextractr)  
library(raster)
library(terra)
library(sf)
library(lubridate)
library(dplyr)
library(arrow)
library(rstudioapi)
library(stringr)
library(dataPreparation)


#---------------------------------------------------------------------------------------------#
sources = c("AUXIL", "CRU", "UDELA", "ERA5", "SPEI")

for (s in sources){
  print(s)
  dirname(rstudioapi::getActiveDocumentContext()$path) %>% setwd()
  source(paste0(s, ".r"))
  print("----------------------------------------")
}
