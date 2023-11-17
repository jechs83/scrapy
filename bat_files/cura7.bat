@echo off

rem Set the number of times to run the spider
set num_runs=100000000000000000000000000

rem Loop to run the spider multiple times
Title Cura 7 Console

cd C:\Git\scrapy\curacao\curacao\spiders\

for /l %%i in (1,1,%num_runs%) do (
    scrapy crawl cura -a u=7 -a b=0
)
