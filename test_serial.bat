REM how to run: ./test_serial.bat

@echo off
REM define variables
set COM_PORT = COM15
set BAUD_RATE = 115200

( 
    for /l %%x in (1, 1, 4) do (
        echo %%x
        timeout /t 2 >nul
    )
) | plink.exe -batch -v -serial COM15 -sercfg 115200,8,1,n,N