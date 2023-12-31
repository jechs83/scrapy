
Title metro 1 Console

rem Loop to run the spider multiple times

cd C:\Git\scrapy\metro\metro\spiders\

:loop
scrapy crawl metro1 -a u=1 -a b=0
goto loop

