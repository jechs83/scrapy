
Title plazavea 6 Console

rem Loop to run the spider multiple times

cd C:\Git\scrapy\plazavea\plazavea\spiders\

:loop
scrapy crawl oh -a u=6 -a b=0
goto loop

