import requests
import json

# Send an HTTP GET request to the URL
url = 'https://shopstar.pe/tecnologia/televisores'
response = requests.get(url)

print(response)

# Check if the request was successful
if response.status_code == 200:
    # Extract the HTML content from the response
    html_content = response.text
    print("se encontro web")
   

    # Find the starting and ending indices of the JSON data within the HTML template
    start_index = html_content.find('{"__STATE__":')
    print(start_index)
    end_index = html_content.find('</script>', start_index)

    # Extract the JSON data string from the HTML template
    json_data = html_content[start_index:end_index]

    # Parse the JSON data into a Python dictionary
    data_object = json.loads(json_data)

    # Now you can access the data using the 'data_object' variable
    print(data_object)
else:
    print('Failed to retrieve data from the URL')
