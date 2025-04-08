@echo off
mkdir out_main2
for /L %%i in (0,1,99) do (
    setlocal enabledelayedexpansion
    set idx=0000%%i
    set idx=!idx:~-4!
    echo Processing input file in\!idx!.txt...
    tester.exe "C:\Users\iwamu\AppData\Local\mise\installs\python\3.13.2\python.exe" main2.py < in\!idx!.txt > out_main2\!idx!.txt
    echo !idx! finish
    endlocal
)
