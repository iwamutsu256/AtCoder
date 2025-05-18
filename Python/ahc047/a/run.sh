#!/bin/bash

for i in $(seq -w 0000 0099); do
    time python main_hirosegolf.py < in/${i}.txt > out_h/${i}.txt
done
