from bs4 import BeautifulSoup
import json
import requests

url = "https://www.plazavea.com.pe/tecnologia/computo?page=13"


def get_json(web):
    # Make an HTTP request
    response = requests.get(web)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the script tag
        script_tag = soup.find_all('script', {'type': 'text/javascript', 'language': 'javascript'})

    for i,v in enumerate(script_tag):
        if i ==1:
            data = v.get_text()

    json_start = data.find('{')
    json_end = data.rfind('}') + 1
    json_data = data[json_start:json_end]
    json_data = json.loads(json_data)

    category = str(json_data["categoryId"])
    department = str(json_data["departmentyId"])
    url = "https://www.plazavea.com.pe/api/catalog_system/pub/products/search?fq=C:/"+department+"/"+category
#https://www.plazavea.com.pe/api/catalog_system/pub/products/search?fq=C:/678/687/&_from=21&_to=41&O=OrderByScoreDESC&

    return url
        
