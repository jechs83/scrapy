

rem Loop to run the spider indefinitely
Title Juntoz 1 Console

cd C:\Git\scrapy\juntoz\juntoz\spiders\

:loop
scrapy crawl jun -a u=1 -a b=0
goto loop

