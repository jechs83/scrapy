import schedule
import time
import subprocess

def run_batch_file():
    subprocess.call([r'C:\Git\scrapy\bat_files\platanitos1.bat'])
    

# Schedule the task to run every 10 minutes
schedule.every(1).minutes.do(run_batch_file)

# Infinite loop to run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)