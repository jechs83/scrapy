
Title wong 1 Console

rem Loop to run the spider multiple times

cd C:\Git\scrapy\wong\wong\spiders\

:loop
scrapy crawl wo -a u=1 -a b=0
goto loop
