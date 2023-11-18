
Title plazavea 2 Console

rem Loop to run the spider multiple times

cd C:\Git\scrapy\plazavea\plazavea\spiders\

:loop
scrapy crawl oh -a u=2 -a b=0
goto loop

