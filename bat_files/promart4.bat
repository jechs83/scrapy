
Title promart 4 Console

rem Loop to run the spider multiple times

cd C:\Git\scrapy\promart\promart\spiders\

:loop
scrapy crawl pro -a u=4 -a b=0
goto loop
