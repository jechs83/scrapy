@echo off

rem Set the number of times to run the spider
set num_runs=10000

rem Loop to run the spider multiple times



cd C:\Git\scrapy\demo\demo\spiders\

for /l %%i in (1,1,%num_runs%) do (
    scrapy crawl saga -a u=8 -a b=0
)
