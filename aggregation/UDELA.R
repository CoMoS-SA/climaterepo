### ------------------------------------------------------------------------------- ###

#                                         UDELA                                     #

### ------------------------------------------------------------------------------  ####

yeardens= c("2000", "2005", "2010", "2015")

climvars = c("tmp", "pre")
weights = c("un", "pop", "lights", "cropl", "concurrent")
resolutions = c("gadm0", "gadm1")

dict_save = list(pop = "pop", un = "un", lights = "lights", cropl = "cropland", concurrent = "concurrent")
dict_var = list(tmp = "temperature", pre = "precipitazioni")
dict_var_tar = list(tmp = "air_temp", pre = "precip")

dirname(rstudioapi::getActiveDocumentContext()$path) %>% dirname()%>% setwd()

# import the temperature and precipitation data from UDELA
for (var in climvars){
  
  # Read the first year
  udel = read.table(
    paste0("Data_Sources/UDELA/", toupper(var),"/", dict_var_tar[[var]], ".1900"), 
    sep = "", 
    header = F,
    na.strings ="", stringsAsFactors= F)[1:14]
  colonne = c('long', 'lat', 'jan1900', 'feb1900', 'mar1900', 'apr1900','may1900', 'jun1900', 'jul1900', 'aug1900', 'sep1900', 'oct1900', 'nov1900', 'dec1900')
  colnames(udel) <-  colonne
  
  for (i in 1901:2017){
    temp = read.table(
      paste0("Data_Sources/UDELA/", toupper(var),"/", dict_var_tar[[var]], ".", as.character(i)), 
      sep = "" , 
      header = F ,
      na.strings ="", stringsAsFactors= F)
    temp = temp[, 3:(length(temp)-1)] # not read the lat and long
    colnames(temp) = paste0(months, as.character(i))
    udel = cbind(udel, temp) # create unique dataset. Row: latlon point in the Earth. Column: total precipitation in month-year
  } 

  # add complementary row to create a complete raster 
  compl_row <- list(long=179.75, lat=89.75)
  udel2 = udel
  udel2[nrow(udel2) + 1, names(compl_row)] <- compl_row
  
  #create layers for the raster of the precipitations
  rasterone <- rasterFromXYZ(udel2[,1:3])
  for (i in 4:ncol(udel2)){
    rasterino <- rasterFromXYZ(udel2[,c(1:2,i)])
    rasterone <- addLayer(rasterone, rasterino)
  }
  
  crs(rasterone) = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs+ towgs84=0,0,0"

  for (d in yeardens){
    for (w in weights){
      if (w == "un"){
        weight = 1
      } else if (w == "concurrent"){
        weight = 1
      } else {
        weight <- get(
          paste0(
            w,
            "50",
            d
          )
        )
      }
      
      if (w %in% c("un", "concurrent") & d %in% c("2005", "2010", "2015")){
        next
      }
      
      for (res in resolutions){
        print(var)
        print(d)
        print(w)
        print(res)
        
        if (w == "concurrent"){
          agg = list()
          for (deca in 190:201){
            print(deca)
            print("....")
            decachar = as.character(deca)
            weight = paste0("popc50", decachar, "0") %>% get()
            cols = names(rasterone)
            subcols = cols[grepl(decachar, cols)]
            rasteronedeca = subset(rasterone, subcols) %>% brick()
            agg[[decachar]] = exact_extract(rasteronedeca, get(res), fun = "weighted_mean", weights = weight)
          }
          agg = do.call(cbind, agg)
        } else if (w == "cropl"){
          agg = exact_extract(rasterone, get(res), fun = "weighted_mean", weights = weight)
        } else {
          agg = exact_extract(rasterone, get(res), fun = "weighted_mean", weights = area(rasterone)*weight)
        }
        agg2 = cbind(get(paste0(res, "_poly")), agg)
        count = 2
        for (i in 1900:2017){
          colnames(agg2)[c(count:(count+11))] = paste0("X", as.character(i), months)
          count = count +12
        }
        
        # Transpose 
        agg2.names = agg2[[1]]
        agg3 = t(agg2[,-1])%>% data.frame()
        colnames(agg3) = agg2.names
        Date = row.names(agg3)
        agg3 = cbind(Date, agg3) %>% fast_round(digits = 2)
        colnames(agg3) = gsub("\\.", "_", colnames(agg3))
        
        year_save = d
        if(w %in% c("un", "concurrent")) year_save = ""
        
        write_parquet(agg3, 
                      paste0(
                        "Data_Final/",
                        res,
                        "_dela_",
                        var,
                        "_",
                        dict_save[[w]], 
                        "_",
                        year_save,
                        "_",
                        "monthly",
                        ".parquet"
                      ))
        
      }
    }
  }
}
      
rm(udel)
rm(udel2)
rm(rasterone)
