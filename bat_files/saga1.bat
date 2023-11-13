

@echo off

rem Loop to run the spider indefinitely
:loop
cd C:\Git\scrapy\demo\demo\spiders\
scrapy crawl saga -a u=3 -a b=0

rem Pause for a few seconds (adjust the time as needed)
timeout /t 5 /nobreak

rem Jump back to the beginning of the loop
goto :loop