import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# Supongamos que tienes una colección de MongoDB llamada "productos" con los campos mencionados.
# Puedes cargar estos datos en un DataFrame de Pandas para el procesamiento.
# Aquí, usamos un DataFrame de ejemplo:

data = {
    'Producto': ['Televisor', 'Celular', 'Tablet', 'Laptop', 'Cámara'],
    'Marca': ['Sony', 'Samsung', 'Apple', 'HP', 'Canon'],
    'PrecioLista': [1000, 800, 500, 1200, 300],
    'PrecioDescuento': [900, 750, 450, 1100, 250],
    'PrecioTarjeta': [850, 700, 430, 1080, 240]
}

df = pd.DataFrame(data)

# Selecciona las columnas relevantes para el modelo (en este caso, PrecioLista, PrecioDescuento y PrecioTarjeta).
X = df[['PrecioLista', 'PrecioDescuento', 'PrecioTarjeta']]

# Normaliza los datos para que tengan media 0 y desviación estándar 1.
scaler = StandardScaler()
X_normalized = scaler.fit_transform(X)

# Entrena un modelo de Isolation Forest para detectar anomalías.
model = IsolationForest(contamination=0.05)  # Puedes ajustar la contaminación según tus criterios.

# Ajusta el modelo a los datos.
model.fit(X_normalized)

# Predice anomalías en los datos.
predictions = model.predict(X_normalized)

# Agrega las predicciones al DataFrame original.
df['Anomalia'] = predictions

# Los productos con 'Anomalia' igual a -1 son considerados anormales.
productos_anormales = df[df['Anomalia'] == -1]

# Muestra los productos anormales.
print("Productos Anormales:")
print(productos_anormales)
