
Title Cura 1 Console

rem Loop to run the spider multiple times

cd C:\Git\scrapy\curacao\curacao\spiders\

:loop
scrapy crawl cura -a u=1 -a b=0
goto loop
