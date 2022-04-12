#!/bin/bash

for FILE in hypothesis_processed/*;
    do
        echo $FILE
        echo $FILE >> results.txt;
        wer reference_processed/$(echo $FILE | cut -d'/' -f 2) $FILE | tee -a results.txt;
#    wer -i reference_processed/$(echo $FILE | cut -d'/' -f 2) $FILE;

done
exit
