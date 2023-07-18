
import concurrent.futures
import subprocess

commands = [
    'C:\GIT\scrapy" cmd /k python test_auto.py saga 1 demo',
    'C:\GIT\scrapy" cmd /k python test_auto.py saga 2 demo',
    'C:\GIT\scrapy" cmd /k python test_auto.py saga 3 demo',
]

def run_command(command):
    process = subprocess.Popen(command, shell=True)
    process.wait()
    return command

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(run_command, command) for command in commands]
    for future in concurrent.futures.as_completed(futures):
        finished_command = future.result()
        print(f"Command '{finished_command}' has finished.")

print("All Scrapy commands have finished.")