#!/bin/bash
mkdir out_sample
for i in $(seq -w 0000 0099); do
    time cat ./in/{i}.txt | ./tester.exe "C:\Users\iwamu\AppData\Local\mise\installs\python\3.13.2\python.exe" sample.py > ./sample_out/{i}.txt
done
