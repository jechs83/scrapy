rem Loop to run the spider indefinitely

cd C:\Git\scrapy\platanitos\platanitos\spiders\
:loop
scrapy crawl platano -a u=1 -a b=0
goto loop
