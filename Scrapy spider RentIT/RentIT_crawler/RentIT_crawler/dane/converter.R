library(rjson)
library(data.table)
library(readr)
library(magrittr)
library(stringr)

jsn <- fromJSON(file = "Scrapy flats all.json")


# Lista wszystkich "głównych" kolumn
mainList <- lapply(jsn, names) %>% unlist(.) %>% unique(.) %>% 
  tolower(.) %>% trimws(.)

# Lista pól z cechami szczególnymi lokalu
featureList <- lapply(jsn, '[[', "cechy") %>% lapply(., names) %>% 
  unlist(.) %>% unique(.)

featureListCleared <- featureList %>% gsub(":", "", .) %>% gsub(" ", "_", .) %>% 
  tolower(.) %>% trimws(.)

# Licba zdjęć
photoNum <- lapply(jsn, '[[', "zdjecia") %>% sapply(., length) %>% max(.)

# Utwórz pustą tabelę
emp <- list()
for(jtr in mainList){

  if(jtr == "cechy"){
    for(ntr in featureListCleared){
      emp[[ntr]] <- NA
    }
  } else if(jtr == "zdjecia"){
    for(ntr in seq(1, photoNum)){
      emp[[paste0("zdjecia_", ntr)]] <- NA
    }
  } else{
    emp[[jtr]] <- NA
  }
  
}

table <- as.data.table(emp)

# Załaduj dane do tabeli
for(itr in seq_along(jsn)){
  emp <- list()
  for(jtr in mainList){
    
    if(jtr == "cechy"){
      for(ntr in seq_along(featureList)){
        emp[[featureListCleared[ntr]]] <- jsn[[itr]][[jtr]][[featureList[ntr]]]
      }
    } else if(jtr == "zdjecia"){
        for(ntr in seq_len(photoNum)){
          if(ntr <= length(jsn[[itr]][[jtr]])){
            emp[[paste0("zdjecia_", ntr)]] <- jsn[[itr]][[jtr]][[ntr]]
          } else{
            emp[[paste0("zdjecia_", ntr)]] <- NA
          }
          
        }
    } else{
      emp[[jtr]] <- jsn[[itr]][[jtr]]
    }
    
  }
  table <- rbind(table, as.data.table(emp), fill = TRUE)
}

# Usuń polskie znaki z nazw kolumn
names(table) <- table %>% names(.) %>% iconv(.,from = "UTF-8", to="ASCII//TRANSLIT")

table <- table[-1,]
table$cena <- gsub(',', '.',gsub("\\s", "", gsub("[zł]","",table$cena)))
table$czynsz<- gsub(',', '.',gsub("\\s", "", gsub("[zł]","",table$czynsz)))
table$powierzchnia <- gsub(',', '.',gsub("\\s", "", table$powierzchnia %>% 
                                           sapply(., function(x){
                                             substr(x, 1, nchar(x) - 2)
                                             },
                                             USE.NAMES = FALSE
                                             )))
table$powierzchnia <- as.numeric(table$powierzchnia)
table$cena[grepl("EUR", table$cena)==TRUE] <- as.double(gsub("EUR","", table$cena))*read_csv("https://stooq.pl/q/l/?s=eurpln&f=sd2t2ohlc&h&e=csv")$Otwarcie

table$cena_za_metr <- substr(gsub(',', '.',gsub("\\s", "", gsub("[zł/m]","",table$cena_za_metr))),1,nchar(gsub(',', '.',gsub("\\s", "", gsub("[zł/m]","",table$cena_za_metr))))-1)
table$liczba_wyswietlen <- unlist(str_extract_all(table$liczba_wyswietlen,"\\(?[0-9,.]+\\)?"))
table$rok_budowy <- unlist(str_extract_all(table$rok_budowy,"\\(?[0-9,.]+\\)?"))
table[is.na(table)] <- ""

write_excel_csv(table, "flats_all.csv")
table[, forma_wlasnosci] %>% unique(.)
