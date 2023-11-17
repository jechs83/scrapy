rem Loop to run the spider indefinitely
Title Saga 11 Console

cd C:\Git\scrapy\demo\demo\spiders\

:loop
scrapy crawl saga -a u=11 -a b=0
goto loop
