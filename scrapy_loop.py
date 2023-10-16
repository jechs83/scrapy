import subprocess
import asyncio
import sys
import time

arg_1  = sys.argv[1]
arg_2  = sys.argv[2]
arg_3  = sys.argv[3]
print(arg_1)
print(arg_2)
print(arg_3)

async def run_spider(arg_1, arg_2, arg_3):
    while True:
        # start the Scrapy spider

        path  = "C:\\GIT\\scrapy\\"+arg_3+"\\"+arg_3+"\\spiders"
        process = subprocess.Popen(['scrapy', 'crawl', arg_1, "-a", "u="+str(arg_2)], cwd=path,  creationflags=subprocess.CREATE_NEW_CONSOLE)
        time.sleep(10)
        #process.wait()

        # wait for a few seconds before restarting the spider
        # print(f"{arg_1} - {arg_2} se va a reiniciar en 10 segundos ")
        # await asyncio.sleep(10)




if __name__ == '__main__':
    asyncio.run(run_spider(arg_1,arg_2, arg_3))









