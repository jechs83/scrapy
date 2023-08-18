
urls = [("urla"), ("urlb")]
url = []
for i in urls:
            temp_array = []  # Create a temporary array for each iteration
            for e in range(4):
                temp_array.append(i + str(e + 1))
            url.append(temp_array)  # Append the temporary array to the main list
print(url)

