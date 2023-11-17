rem Loop to run the spider indefinitely
Title Saga 14 Console

cd C:\Git\scrapy\demo\demo\spiders\

:loop
scrapy crawl saga -a u=14 -a b=0
goto loop
