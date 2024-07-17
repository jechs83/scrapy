
Title coolbox 1 Console

rem Loop to run the spider multiple times

cd C:\Git\scrapy\coolbox\coolbox\spiders\

:loop
scrapy crawl cool -a u=1 -a b=0
goto loop
