
Title plazavea 5 Console

rem Loop to run the spider multiple times

cd C:\Git\scrapy\plazavea\plazavea\spiders\

:loop
scrapy crawl oh -a u=5 -a b=0
goto loop
