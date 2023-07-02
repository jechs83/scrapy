import os
import subprocess

user_ids = [100, 200, 300]
spiders_folder = "/Users/javier/GIT/scrapy_saga/demo/demo/spiders"

# Change to the spiders folder
os.chdir(spiders_folder)



# Define the list of values for the 'u' argument
values = [100, 200, 300]

# Run the Scrapy commands in a loop indefinitely
for value in values:
    command = f"scrapy crawl saga -a u={value}"
    subprocess.run(['osascript', '-e', f'tell application "Terminal" to do script "{command}"'])