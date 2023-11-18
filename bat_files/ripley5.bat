
Title ripley 5 Console

rem Loop to run the spider multiple times

cd C:\Git\scrapy\ripley\ripley\spiders\

:loop
scrapy crawl ripley_scrap -a u=5 -a b=0
goto loop