#!/bin/bash

for i in $(seq -w 0000 0099); do
    time python main.py < in/${i}.txt > out/${i}.txt
done
