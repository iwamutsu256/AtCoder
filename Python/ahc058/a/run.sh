#!/bin/bash

for i in $(seq -w 0000 0099); do
    time python main8.py < in/${i}.txt > out8/${i}.txt
done
