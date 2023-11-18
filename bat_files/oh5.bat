
Title Oh 5 Console

rem Loop to run the spider multiple times

cd C:\Git\scrapy\oechsle\oechsle\spiders\

:loop
scrapy crawl oh -a u5 -a b=0
goto loop
