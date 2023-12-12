
### ------------------------------------------------ ###

###                 SPEI                             ###

### ------------------------------------------------ ###
yeardens= c("2000", "2005", "2010", "2015")
weights = c("un", "pop", "lights")
resolutions = c("gadm0", "gadm1")

dict_save = list(pop = "pop", un = "un", lights = "lights")
dict_var = list(tmp = "temperature", pre = "precipitazioni")

dirname(rstudioapi::getActiveDocumentContext()$path) %>% dirname()%>% setwd()

spei = brick("Data_Sources/SPEI/spei01.nc", var="spei", level = 1)

for (d in yeardens){
  for (w in weights){
    if (w == "un"){
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
    for (res in resolutions){
      print("res")
      print(d)
      print(w)
      print(res)
      
      agg = exact_extract(spei, get(res), fun = "weighted_mean", weights = area(spei)*weight)
      agg2 = cbind(get(paste0(res, "_poly")), agg)
      count = 2
      for (i in 1901:2020){
        colnames(agg2)[c(count:(count+11))] = paste0("X", as.character(i), months)
        count = count +12
      }
      
      agg2.names = agg2[[1]]
      agg3 = t(agg2[,-1])%>% data.frame()
      colnames(agg3) = agg2.names
      Date = row.names(agg3)
      agg3 = cbind(Date, agg3)
      colnames(agg3) = gsub("\\.", "_", colnames(agg3))

      year_save = d
      if(w == "un") year_save = ""
      write_parquet(agg3, 
                    paste0(
                      "Data_Final/",
                      res,
                      "_spei_",
                      "spei",
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

rm(spei)