### ------------------------------------------------ ###

###                 ERA5                             ###

### ------------------------------------------------ ###
yeardens= c("2000", "2005", "2010", "2015")
climvars = c("tmp", "pre")
weights = c("un", "pop", "lights")
resolutions = c("gadm0", "gadm1")

dict_save = list(pop = "pop_", un = "un_", lights = "lights_")
dict_var = list(tmp = "t2m", pre = "tp")

dirname(rstudioapi::getActiveDocumentContext()$path) %>% dirname() %>% setwd()

for (var in climvars){
  ERA5 = brick("Data_Sources/ERA5/era5all.nc", var= dict_var[[var]], level = 1)
  crs(ERA5) = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs+ towgs84=0,0,0"
  for (d in yeardens){
    for (w in weights){
      if (w == "un"){
        weight = 1
      } else {
        weight <- get(
          paste0(
            w,
            "25",
            d
          )
        )
        weight = resample(weight, ERA5, method='bilinear')
      }
      for (res in resolutions){
        print(var)
        print(d)
        print(w)
        print(res)
        
        agg = exact_extract(ERA5, get(res), fun = "weighted_mean", weights = area(ERA5)*weight)
        agg2 = agg[, c(1:(83*12))]
        agg2 = cbind(get(paste0(res, "_poly")), agg2)
        
        count = 2
        for (i in 1940:2022){
          colnames(agg2)[c(count:(count+11))] = paste0("X", as.character(i), months)
          count = count +12
        }
        
        cols = names(agg2)
        for (i in 1:ncol(agg2)){
          if (startsWith(cols[i], "X")== TRUE){
            date = as.Date(paste0(cols[i],"01"), format= "X%Y%m%d")
            if (var == "pre"){
              agg2[,i] = agg2[,i]*days_in_month(date)*1000
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
        
        # Transpose
        agg2.names = agg2[[1]]
        agg3 = t(agg2[,-1])%>% data.frame()
        colnames(agg3) = agg2.names
        Date = row.names(agg3)
        agg3 = cbind(Date, agg3)
        colnames(agg3) = gsub("\\.", "_", colnames(agg3))
        
        write_parquet(agg2, 
                      paste0(
                        "Data_Final/",
                        res,
                        "_era_",
                        var,
                        "_",
                        dict_save[[w]], 
                        d, 
                        ".parquet"
                      ))
        
      }
    }
  }
}

rm(ERA5)