
Title Cura 1 Console

rem Loop to run the spider multiple times

cd C:\Git\scrapy\hiraoka\hiraoka\spiders\

:loop
scrapy crawl hira -a u=2 -a b=0
goto loop
