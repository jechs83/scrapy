

rem Loop to run the spider indefinitely

cd C:\Git\scrapy\tailoy\tailoy\spiders\

:loop
scrapy crawl tai -a u=1 -a b=0
goto loop

