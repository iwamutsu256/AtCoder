#!/bin/bash

for i in $(seq -w 0000 0099); do
    time python main10.py < in/${i}.txt > out10/${i}.txt
done
