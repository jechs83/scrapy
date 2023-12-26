rem Loop to run the spider indefinitely
Title SHOP 4 Console

cd C:\Git\scrapy\shopstar\shopstar\spiders\

:loop
scrapy crawl shop -a u=4 -a b=0
goto loop
