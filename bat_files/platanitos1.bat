rem Loop to run the spider indefinitely
Title Platanitos 1 Console

cd C:\Git\scrapy\platanitos\platanitos\spiders\
:loop
scrapy crawl platano -a u=1 -a b=0
goto loop
