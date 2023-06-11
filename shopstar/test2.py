import requests
import json
import re
import time

url = 'https://shopstar.pe/tecnologia/televisores?page=1' # Replace with the actual URL


response = requests.get(url)
if response.status_code == 200:
    html_content = response.text

    # Search for the text content between <script> tags
    pattern = r"<script\b[^>]*>(.*?)</script>"
    matches = re.findall(pattern, html_content, re.DOTALL)
    i=0
    ss=[]
    if matches:
        for match in matches:
            i=i+1
            if i ==12:         
          
                extracted_text = match.strip()
                print(ss.append(extracted_text))
    else:
        print("No text content found between <script> tags.")
else:
    print("Request to the URL failed.")
ss = str(ss)[72:-3]
with open ("text.txt", "w") as f:
    f.write(str(ss))