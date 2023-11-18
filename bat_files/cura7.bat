
Title Cura 7 Console

rem Loop to run the spider multiple times

cd C:\Git\scrapy\curacao\curacao\spiders\

:loop
scrapy crawl cura -a u=7 -a b=0
goto loop
