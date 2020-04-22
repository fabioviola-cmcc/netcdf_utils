#!/bin/bash

# if the output file exists, remove it and create it again
if [ -f $2 ]; then rm $2 ; fi
touch $2

# create the file
for LINE in $(grep -v "[a-z]" $1 | tr -s " " | tr ' ' ',' | cut -d ',' -f 2-)
do
    #    echo $LINE
    TEMP=$LINE
    echo $TEMP
    NUM_COMMAS=$(echo $TEMP | grep "," -o | wc -c)
    if [ $NUM_COMMAS -ge 10 ]; then
    	echo $TEMP >> $2
    fi
done
