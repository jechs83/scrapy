@echo off

rem Set the number of times to run the spider
set num_runs=100000000000000000000000000

rem Loop to run the spider multiple times

cd C:\Git\scrapy\oechsle\oechsle\spiders\

for /l %%i in (1,1,%num_runs%) do (
    scrapy crawl oh -a u=12 -a b=0
)
