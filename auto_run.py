
import subprocess
import time
import sys

import subprocess
def close():
    try:
        print("sads")
        subprocess.run(["taskkill", "/IM", "WindowsTerminal.exe", "/F"])
 
    except:
        print ("Unexpected error:", sys.exc_info())
    


def loop ():
    command2 = ['cmd', '/c', 'start', 'cmd', '/k', 'cd /d C:\\GIT\\scrapy\\ripley\\ripley\\spiders  && scrapy crawl ripley_scrap -a u=0']
    subprocess.Popen(command2)

    for i in range (3):


        command = ['cmd', '/c', 'start', 'cmd', '/k', 'cd /d C:\\GIT\\scrapy\\demo\\demo\\spiders  && scrapy crawl saga -a u='+str(i+1)]
        command2 = ['cmd', '/c', 'start', 'cmd', '/k', 'cd /d C:\\GIT\\scrapy\\curacao\\curacao\\spiders  && scrapy crawl cura -a u='+str(i+1)]

        # Use subprocess.Popen to run the command
        subprocess.Popen(command)
        subprocess.Popen(command2)
       
    time.sleep(800)
    close()
    time.sleep(30)
    loop()

try:
 loop()
except:
    close()
    time.sleep(20)
    loop()
