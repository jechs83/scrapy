import requests
import json
from bs4 import BeautifulSoup


def get_json(web):
    url = web

    try:
        # Step 1: Fetch the HTML content of the webpage
        response = requests.get(url)
        response.raise_for_status()

        # Step 2: Parse the HTML content and extract JSON data
        soup = BeautifulSoup(response.text, "html.parser")
        script_tag = soup.find("script", id="__NEXT_DATA__")

        if script_tag:
            # Extract JSON data from the script tag's content
            json_data = json.loads(script_tag.contents[0])

            # You can now access the JSON data like a dictionary
            print(json_data)

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except AttributeError:
        print("Script tag with id '__NEXT_DATA__' not found in the HTML.")
    with open("json.txt" , "w+") as f:
        f.write(str(json_data))

    return json_data

