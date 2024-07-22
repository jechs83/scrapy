web =  "https://shopstar.pe/api/catalog_system/pub/products/search?"


# Definir el número total de listas y la cantidad de números por lista
total_lists = 20000
numbers_per_list = 50

# Crear el array de listas
array_of_lists = []

for i in range(total_lists):
    start_number = i * numbers_per_list
    array_of_lists.append([f"fq=productId:{num}&" for num in range(start_number, start_number + numbers_per_list)])

url_lista = []
for i in array_of_lists:
    print()
    string_sin_espacios = ''.join(i).replace(" ", "")

    web_final = web+string_sin_espacios

    url_lista.append(web_final)


#print(url_lista)

#https://shopstar.pe/api/catalog_system/pub/products/search?fq=productId:


#&fq=productId:49951&fq=productId:49952&fq=productId:49953&fq=productId:49954&fq=productId:49955&fq=productId:49956&fq=productId:49957&fq=productId:49958&fq=productId:49959&fq=productId:49960&fq=productId:49961&fq=productId:49962&fq=productId:49963&fq=productId:49964&fq=productId:49965&fq=productId:49966&fq=productId:49967&fq=productId:49968&fq=productId:49969&fq=productId:49970&fq=productId:49971&fq=productId:49972&fq=productId:49973&fq=productId:49974&fq=productId:49975&fq=productId:49976&fq=productId:49977&fq=productId:49978&fq=productId:49979&fq=productId:49980&fq=productId:49981&fq=productId:49982&fq=productId:49983&fq=productId:49984&fq=productId:49985&fq=productId:49986&fq=productId:49987&fq=productId:49988&fq=productId:49989&fq=productId:49990&fq=productId:49991&fq=productId:49992&fq=productId:49993&fq=productId:49994&fq=productId:49995&fq=productId:49996&fq=productId:49997&fq=productId:49998&fq=productId:49999&>