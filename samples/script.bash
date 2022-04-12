#!/bin/bash

for FILE in hypothesis_processed/*;
    do
        echo $FILE
        echo $FILE >> results_confusion.txt;
        wer -c reference_processed/$(echo $FILE | cut -d'/' -f 2) $FILE | tee -a results_confusion.txt;
#    wer -i reference_processed/$(echo $FILE | cut -d'/' -f 2) $FILE;

done
exit
