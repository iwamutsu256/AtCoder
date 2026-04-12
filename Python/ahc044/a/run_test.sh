#!/bin/bash

for i in $(seq -w 0000 0099); do
    time python main999.py < in/${i}.txt > out999/${i}.txt
done
