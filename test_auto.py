import subprocess
import asyncio

async def run_spider(scrap, num):
    while True:
        # start the Scrapy spider
        process = subprocess.Popen(['scrapy', 'crawl', scrap, "-a", "u="+str(num)], cwd='C:\GIT\scrapy\demo\demo\spiders',  creationflags=subprocess.CREATE_NEW_CONSOLE)
        process.wait()
        
        # wait for a few seconds before restarting the spider
        print(f"{scrap} - {num} se va a reiniciar en 10 segundos ")
        await asyncio.sleep(10)
        
        
async def main():
    # create tasks for each spider and number combination
    tasks = [
        asyncio.create_task(run_spider('saga', 1)),
        asyncio.create_task(run_spider('saga', 2)),
    ]

    # run the tasks concurrently
    await asyncio.gather(*tasks)
    

if __name__ == '__main__':
    asyncio.run(main())
