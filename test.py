import requests
from bs4 import BeautifulSoup

url = 'https://simple.ripley.com.pe'

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all the anchor tags (links) in the HTML
links = soup.find_all('a')

# Extract and print the href attribute of each link
for link in links:
    href = link.get('href')
    if href:
        print(href)