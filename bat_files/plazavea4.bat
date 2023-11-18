
Title plazavea 4 Console

rem Loop to run the spider multiple times

cd C:\Git\scrapy\plazavea\plazavea\spiders\

:loop
scrapy crawl vea -a u=4 -a b=0
goto loop

