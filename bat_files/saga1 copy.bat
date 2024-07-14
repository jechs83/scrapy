rem Loop to run the spider tasks indefinitely with error handling and delay
title Saga 1 Console

cd C:\Git\scrapy\demo\demo\spiders\

:loop
start cmd /k "scrapy crawl saga -a u=1 -a b=0"
start cmd /k "scrapy crawl saga -a u=2 -a b=0"

rem Wait for a while before restarting the tasks
timeout /t 10

goto loop
