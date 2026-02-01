#!/bin/bash

for i in $(seq -w 0000 0099); do
    time python main7.py < in/${i}.txt > out7/${i}.txt
done
