import subprocess

# Replace 'other_script.py' with the name of your Python file
file_to_execute = '/Users/javier/GIT/scrapy_saga/demo/saga_s.py'

# Run the Python file using subprocess
subprocess.run(['python', file_to_execute])
# import subprocess

# # Replace 'other_script.py' with the name of your Python file
# file_to_execute = '/Users/javier/GIT/scrapy_saga/demo/saga_s.py'

# # Run the Python file using subprocess
# subprocess.run(['python', file_to_execute])



from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from shopstar.spiders.shop import ShopSpider
import subprocess

file_to_execute = '/Users/javier/GIT/scrapy_saga/shopstar/test_links.py'

def run_spider_with_parameters( ):

    process = subprocess.run(['python', file_to_execute,"1"])
    process = subprocess.run(['python', file_to_execute, "2"])
    process = subprocess.run(['python', file_to_execute,"3"])
    process = subprocess.run(['python', file_to_execute, "4"])
    process = subprocess.run(['python', file_to_execute,"5"])
    process = subprocess.run(['python', file_to_execute, "6"])
    process = subprocess.run(['python', file_to_execute, "7"])

 


if __name__ == "__main__":


    run_spider_with_parameters()
    subprocess.run("pkill -f 'python test_links.py'")


