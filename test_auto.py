import subprocess

def run_processes():
    while True:
      
        
        tailoy = ['cmd', '/c', 'start', 'cmd', '/k', 'cd /d C:\\GIT\\scrapy\\tailoy\\tailoy\\spiders  && scrapy crawl tai -a u=1']
        subprocess.Popen(tailoy).wait()
    
if __name__ == '__main__':
    run_processes()
