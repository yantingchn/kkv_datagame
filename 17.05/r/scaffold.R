list.of.packages <- c("stringr", "data.table", "dplyr")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages)) install.packages(new.packages)

library(data.table)
library(stringr)
library(dplyr)

##' load data
train_events <- fread("./data/events_train.csv")
train_labels <- fread("./data/labels_train.csv")
test_events <- fread("./data/events_test.csv")
sample_labels <- fread("./data/sample.csv")

##' set title.id equal to 1 for every users
title.id <- "0"
submission <- sample_labels %>% as.data.frame()

##' add leading zero
submission$user_id <- str_pad(submission$user_id, 8, pad = "0")
submission$title_id <- str_pad(title.id, 8, pad = "0")

##' write to csv
write.csv(submission, "./data/results_1.csv", row.names = F)
