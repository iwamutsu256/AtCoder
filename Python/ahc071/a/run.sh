#!/bin/bash

for i in $(seq -w 0000 0099); do
    time python main5.py < in/${i}.txt > out5/${i}.txt
done
