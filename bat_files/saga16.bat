rem Loop to run the spider indefinitely
Title Saga 16 Console

cd C:\Git\scrapy\demo\demo\spiders\

:loop
scrapy crawl saga -a u=16 -a b=0
goto loop
