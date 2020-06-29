#!/bin/bash

# if the output file exists, remove it and create it again
if [ -f $2 ]; then rm $2 ; fi

# create the file
cat $1 | grep -v "[a-z]" | tail -n +2 | tr -s " " | tr " " "," | sed s/^,// > $2
