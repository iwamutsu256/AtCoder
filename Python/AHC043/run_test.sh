#!/bin/bash

for i in $(seq -w 0000 0099); do
    time python A9.py < test_case/${i}.txt > A9_out/${i}.txt
done
