

### -------------------------------------------###

##                   CRU TS                     ##

### --------------------------------------------##


yeardens= c("2000", "2005", "2010", "2015")

climvars = c("tmp", "pre")
weights = c("un", "pop", "lights", "cropl", "concurrent")
resolutions = c("gadm0", "gadm1")

dict_save = list(pop = "pop", un = "un", lights = "lights", cropl = "cropland", concurrent = "concurrent")
dict_var = list(tmp = "temperature", pre = "precipitazioni")

dirname(rstudioapi::getActiveDocumentContext()$path) %>% dirname() %>% setwd()


for (var in climvars){
  file = paste0(
    "cru_ts4.07.1901.2022.",
    var,
    ".dat.nc"
  )

  brickcru = brick(paste0("Data_Sources/CRU/", file), var=var)
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
          for (deca in 190:202){
            print(deca)
            print("....")
            decachar = as.character(deca)
            weight = paste0("popc50", decachar, "0") %>% get()
            cols = names(brickcru)
            subcols = cols[grepl(decachar, cols)]
            brickcrudeca = subset(brickcru, subcols) %>% brick()
            agg[[decachar]] = exact_extract(brickcrudeca, get(res), fun = "weighted_mean", weights = weight)
          }
          agg = do.call(cbind, agg)
        } else if (w == "cropl"){
          agg = exact_extract(brickcru, get(res), fun = "weighted_mean", weights = weight)
        } else {
          agg = exact_extract(brickcru, get(res), fun = "weighted_mean", weights = area(brickcru)*weight)
        }
        

        agg2 = cbind(get(paste0(res, "_poly")), agg)
        count = 2
        for (i in 1901:2022){
          colnames(agg2)[c(count:(count+11))] = paste0("X", as.character(i), months)
          count = count + 12
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
                    "_cru_",
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

rm(brickcru)
