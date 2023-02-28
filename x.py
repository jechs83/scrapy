
import subprocess
import time

# Iniciar el proceso

command4 = ['cmd', '/c', 'start', 'cmd', '/k', 'cd /d C:\\GIT\\scrapy\\metro\\metro\\spiders  && scrapy crawl metro1 -a u=1']

proc = subprocess.Popen([command4])

# Esperar un momento para que el proceso se inicie completamente
time.sleep(1)

# Capturar el PID del proceso
pid = proc.pid

# Imprimir el PID del proceso
print(f"PID del proceso: {pid}")

# Terminar el proceso
proc.terminate()

# Esperar a que el proceso termine completamente
proc.wait()

# Reiniciar el proceso
proc = subprocess.Popen([command4])