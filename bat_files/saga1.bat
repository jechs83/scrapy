rem Loop to run the spider indefinitely

cd C:\Git\scrapy\demo\demo\spiders\

:loop
scrapy crawl saga -a u=1 -a b=0
goto loop
