import requests
from bs4 import BeautifulSoup
import json
import time
# URL of the web page
url = "https://www.realplaza.com/coleccion/todo-tecnologia?page=1"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the element with the specified data-type and data-varname
    element = soup.find('template', {'data-type': 'json', 'data-varname': '__STATE__'})

    #element = soup.find('template', {'data-type': 'json', 'data-varname': "__RUNTIME__"})



    # Extract text from the element
    if element:
        # Assuming the text is contained within a <script> tag
        script_text = element.find('script').text

        # with open("json.txt" ,"+w") as h:
        #     h.write(script_text)

        # Print or process the extracted text

    else:
        print("Element not found on the page.")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")


data = json.loads(script_text)

for product_key, product_info in data.items():
   
    try:
        id  = "$Product:"+product_info['linkText']+".priceRange.sellingPrice"
    except: id = "None"

   
    print(id)
    print(product_key)
    print()
  
    # if product_key in id:
    #        print(product_info["lowPrice"])




#     try:
#         product = product_info['productName']
#         brand = product_info['brand']
#         sku = product_info["productReference"]
#         link = product_info['link'] 

        
  
#         print(product)
#         print(brand)
#         print(sku)
#         print(link)
#         print()
    
#         # # print(best_price)
#     except:
#         continue
    
   
  
    
  

#     # list_price =product_info
#     # print(list_price)
                

# # for i, v in data.items():

# #     if "Product" in i:
# #         if "productId" in v:
# #             print(v)
# #             print()