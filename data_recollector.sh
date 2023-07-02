#!/bin/bash

while true; do
  # Change to the directory containing your Scrapy project

  # Restart the first Scrapy process
  while true; do
    osascript -e 'tell app "Terminal" to do script "cd /Users/ussdiscovery/Scrap/scrapy/demo/demo/spiders && scrapy crawl saga -a u=100"'
    sleep 10  # Delay before restarting the process (e.g., 10 seconds)
  done &

  # Restart the second Scrapy process
  while true; do
    osascript -e 'tell app "Terminal" to do script "cd /Users/ussdiscovery/Scrap/scrapy/demo/demo/spiders && scrapy crawl saga -a u=200"'
    sleep 30  # Delay before restarting the process (e.g., 10 seconds)
  done &

#   # Restart the third Scrapy process
#   while true; do
#     osascript -e 'tell app "Terminal" to do script "cd /Users/ussdiscovery/Scrap/scrapy/demo/demo/spiders && scrapy crawl saga -a u=300"'
#     sleep 10  # Delay before restarting the process (e.g., 10 seconds)
#   done &

#   # Restart the fourth Scrapy process
#   while true; do
#     osascript -e 'tell app "Terminal" to do script "cd /Users/ussdiscovery/Scrap/scrapy/ripley/ripley/spiders && scrapy crawl ripley_scrap -a u=100"'
#     sleep 10  # Delay before restarting the process (e.g., 10 seconds)
#   done &

  # Wait for all processes to finish before restarting
  wait
done
