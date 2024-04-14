rem Loop to run the spider indefinitely
Title Saga 22 Console

cd C:\Git\scrapy\demo\demo\spiders\

:loop
scrapy crawl saga -a u=22 -a b=0
goto loop
