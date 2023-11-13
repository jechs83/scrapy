@echo off

rem Set the number of times to run the spider
set num_runs=10000

rem Loop to run the spider multiple times



cd C:\Git\scrapy\tailoy\promatailoyrt\spiders\

for /l %%i in (1,1,%num_runs%) do (
    scrapy crawl tai -a u=1 -a b=0
)
