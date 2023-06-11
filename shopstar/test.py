# import requests
# import json

# url = 'https://shopstar.pe/tecnologia/televisores?page=5'
# headers = {
#     'Accept': 'application/json'  # Set the Accept header to indicate JSON response
# }

# response = requests.get(url, headers=headers)


# # Check the response content
# content = response.content.decode('utf-8')
# print(content)

# # Extract the JSON portion from the response content
# json_start = content.find('{')  # Find the start of the JSON
# json_end = content.rfind('}') + 1  # Find the end of the JSON
# json_data = content[json_start:json_end]

# # Parse the extracted JSON data
# try:
#     parsed_json = json.loads(json_data)
#     # Process the parsed JSON data
#     # ...

#     # Example: Print the parsed JSON to the console
#     print(parsed_json)
# except json.JSONDecodeError as e:
#     print(f"Error parsing JSON: {e}")


import requests
import json
import time
import re
import json


r = requests.get('https://shopstar.pe/tecnologia/televisores?page=5')
# you can use r.content to print the webpage data

f=r.content


  
# json.loads(data) `json_loads` is to convert data into `json string`
#print (json.loads(r.content))
# f= r.content

# with open("output.txt", "w") as file:
#     file.write(str(f))



text = str(f)
print(text)

# Search for JSON pattern using regular expression
json_pattern = r"\{.*\}"

matches = re.findall(json_pattern, text, re.DOTALL)

if matches:
    # Extract the first JSON match
    json_data = matches[0]

    # Parse the JSON data
    json_obj = json.loads(json_data)

    print(json_obj)
else:
    print("No JSON format found in the text.")