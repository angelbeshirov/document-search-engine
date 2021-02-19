#!/bin/bash

# path="/home/angel/Desktop/AI/IR/Data/1883-1884"

# python index_files.py \
#         --path=$path

declare -a paths=("/home/angel/Desktop/AI/IR/Data/1881-1882" 
                "/home/angel/Desktop/AI/IR/Data/1882-1883"  
                "/home/angel/Desktop/AI/IR/Data/1883-1884"
        )

## now loop through the above array
for path in "${paths[@]}"
do
        python index_files.py \
                 --path="$path"
done