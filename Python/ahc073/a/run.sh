#!/bin/bash

for i in $(seq -w 0000 0099); do
    time python main3.py < in/${i}.txt > out3/${i}.txt
done
