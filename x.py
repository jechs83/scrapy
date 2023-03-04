
import subprocess

command = ['cmd', '/c', 'start', 'cmd', '/k', 'cd /d C:\\GIT\\scrapy\\metro\\metro\\spiders  && scrapy crawl metro1 -a u=1']

# start the subprocess
proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
pid1 = proc.pid
print(pid1)

# wait for the subprocess to complete and get its output
stdout, stderr = proc.communicate()
print(stdout)
print(type(stdout))
e = str(stdout)
    
    
if  e == "b''":
    print("Subprocess ended.")
    loop()
loop()


# do something else after the subprocess completes
