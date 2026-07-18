#!/bin/bash

for i in $(seq -w 0000 0149); do
    time python main6.py < in/${i}.txt > out6/${i}.txt
done
