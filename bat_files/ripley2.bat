@echo off

rem Set the number of times to run the spider
set num_runs=100000000000000000000000000

rem Loop to run the spider multiple times
Title Ripley 2 Console

cd C:\Git\scrapy\ripley\ripley\spiders\

for /l %%i in (1,1,%num_runs%) do (
    scrapy crawl ripley_scrap -a u=2 -a b=0
)
