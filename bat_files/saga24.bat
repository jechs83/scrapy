rem Loop to run the spider indefinitely
Title Saga 24 Console

cd C:\Git\scrapy\demo\demo\spiders\

:loop
scrapy crawl saga -a u=24 -a b=0
goto loop
