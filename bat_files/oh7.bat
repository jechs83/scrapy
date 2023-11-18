
Title Oh 7 Console

rem Loop to run the spider multiple times

cd C:\Git\scrapy\oechsle\oechsle\spiders\

:loop
scrapy crawl oh -a u=7 -a b=0
goto loop
