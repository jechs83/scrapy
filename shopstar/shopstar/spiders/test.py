web =  "https://shopstar.pe/api/catalog_system/pub/products/search?"


# Definir el número total de listas y la cantidad de números por lista
total_lists = 2000
numbers_per_list = 50

# Crear el array de listas
array_of_lists = []

for i in range(total_lists):
    start_number = i * numbers_per_list
    array_of_lists.append([f"fq=productId:{num}&" for num in range(start_number, start_number + numbers_per_list)])

# Imprimir el resultado
for sublist in array_of_lists:
    print(sublist)


url_lista = []
for i in array_of_lists:
    print()
    string_sin_espacios = ''.join(i).replace(" ", "")

    web_final = web+string_sin_espacios

    url_lista.append(web_final)


print(url_lista)