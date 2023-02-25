
import subprocess
import time
import sys



command = ['cmd', '/c', 'start', 'cmd', '/k', 'cd /d C:\\GIT\\scrapy\\demo\\demo\\spiders  && scrapy crawl saga -a u=3']
process = subprocess.Popen([command] subprocess.Popen(command2)shell=True, executable="C:\WINDOWS\system32\cmd.exe")

       
       
   
def cleanup():
    process.terminate()

import atexit
atexit.register(cleanup) 