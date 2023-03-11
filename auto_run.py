
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
    tailoy = ['cmd', '/c', 'start', 'cmd', '/k', 'cd /d C:\\GIT\\scrapy\\tailoy\\tailoy\\spiders  && scrapy crawl tai -a u=1']
    subprocess.Popen(tailoy)
    command2 = ['cmd', '/c', 'start', 'cmd', '/k', 'cd /d C:\\GIT\\scrapy\\ripley\\ripley\\spiders  && scrapy crawl ripley_scrap -a u=1']
    subprocess.Popen(command2)
    command4 = ['cmd', '/c', 'start', 'cmd', '/k', 'cd /d C:\\GIT\\scrapy\\metro\\metro\\spiders  && scrapy crawl metro1 -a u=1']
    subprocess.Popen(command4)
    command5 = ['cmd', '/c', 'start', 'cmd', '/k', 'cd /d C:\\GIT\\scrapy\\curacao\\curacao\\spiders && scrapy crawl cura -a u=10']
    subprocess.Popen(command5)

    oechsle1 = ['cmd', '/c', 'start', 'cmd', '/k', 'cd /d C:\\GIT\\scrapy\\oechsle\\oechsle\\spiders  && scrapy crawl oh -a u=1']
    subprocess.Popen(oechsle1)
    oechsle2 = ['cmd', '/c', 'start', 'cmd', '/k', 'cd /d C:\\GIT\\scrapy\\oechsle\\oechsle\\spiders  && scrapy crawl oh -a u=2']
    subprocess.Popen(oechsle2)

    for i in range (3):


        command = ['cmd', '/c', 'start', 'cmd', '/k', 'cd /d C:\\GIT\\scrapy\\demo\\demo\\spiders  && scrapy crawl saga -a u='+str(i+1)]
        command3 = ['cmd', '/c', 'start', 'cmd', '/k', 'cd /d C:\\GIT\\scrapy\\shopstar\\shopstar\\spiders  && scrapy crawl shop -a u='+str(i+1)]


        # Use subprocess.Popen to run the command
        subprocess.Popen(command)
        subprocess.Popen(command3)
       
    time.sleep(60 * 20)
    close()
    time.sleep(30)
    loop()

try:
 loop()
except:
    close()
    time.sleep(20)
    loop()
