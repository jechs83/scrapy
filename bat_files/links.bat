@echo off
setlocal enabledelayedexpansion

cd c:\Git\scrapy\shopstar

for /L %%i in (1, 1, 7) do (
    start cmd /k "python test_links.py %%i"
)

endlocal
