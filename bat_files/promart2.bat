
Title promart 2 Console

rem Loop to run the spider multiple times

cd C:\Git\scrapy\promart\promart\spiders\

:loop
scrapy crawl pro -a u=2 -a b=0
goto loop
