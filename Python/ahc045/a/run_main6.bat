@echo off
mkdir out_main6
for /L %%i in (0,1,99) do (
    setlocal enabledelayedexpansion
    set idx=0000%%i
    set idx=!idx:~-4!
    echo Processing input file in\!idx!.txt...
    tester.exe "C:\Users\iwamu\AppData\Local\Programs\Python\Python313\python.exe" main6.py < in\!idx!.txt > out_main6\!idx!.txt
    echo !idx! finish
    endlocal
)
