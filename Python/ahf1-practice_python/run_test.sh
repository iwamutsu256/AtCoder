#!/bin/bash
#ビジュアライザで見れない

for i in $(seq -w 0000 0099); do
    time python 01_nearest_neighbor.py < in/${i}.txt > out01/${i}.txt
done
