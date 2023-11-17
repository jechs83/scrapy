

rem Loop to run the spider indefinitely
Title Tailoy 3 Console

cd C:\Git\scrapy\tailoy\tailoy\spiders\

:loop
scrapy crawl tai -a u=3 -a b=0
goto loop

