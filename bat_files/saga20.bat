rem Loop to run the spider indefinitely
Title Saga 20 Console

cd C:\Git\scrapy\demo\demo\spiders\

:loop
scrapy crawl saga -a u=20 -a b=0
goto loop
