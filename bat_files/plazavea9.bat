@echo off

rem Set the number of times to run the spider
set num_runs=100000000000000000000000000

rem Loop to run the spider multiple times

Title Plazavea 9 Console


cd C:\Git\scrapy\plazavea\plazavea\spiders\

for /l %%i in (1,1,%num_runs%) do (
    scrapy crawl vea -a u=9 -a b=0
)
