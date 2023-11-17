rem Loop to run the spider indefinitely
Title Saga 6 Console

cd C:\Git\scrapy\demo\demo\spiders\

:loop
scrapy crawl saga -a u=6 -a b=0
goto loop
