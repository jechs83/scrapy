


from pymongo import MongoClient, UpdateOne

def actualizar_producto(db, collection_name, sku, new_best_price, new_web_dsct):
    collection = db[collection_name]

    # Definir la actualización para los campos específicos
    updates = {
        "best_price": new_best_price,
        "web_dsct": new_web_dsct
    }

    # Crear la operación de actualización
    update_operation = UpdateOne(
        {"sku": sku},  # Filtro por SKU
        {"$set": updates}  # Actualizar los campos especificados
    )

    # Ejecutar la operación de actualización
    result = collection.bulk_write([update_operation])

    return result.modified_count  # Retorna el número de documentos modificados

# Conexión a la base de datos MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["nombre_de_tu_base_de_datos"]  # Reemplaza "nombre_de_tu_base_de_datos" por el nombre de tu base de datos

# Llamada a la función para actualizar el producto
sku_a_actualizar = "SKU_del_producto_a_actualizar"
nuevo_best_price = 29.99  # Reemplaza con el nuevo valor para best_price
nuevo_web_dsct = 0.1  # Reemplaza con el nuevo valor para web_dsct

# Llamada a la función de actualización
cantidad_modificados = actualizar_producto(db, "nombre_de_tu_coleccion", sku_a_actualizar, nuevo_best_price, nuevo_web_dsct)
print(f"Se han actualizado {cantidad_modificados} documentos.")
