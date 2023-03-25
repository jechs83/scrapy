import matplotlib.pyplot as plt
import mpld3

# Datos de ejemplo
precios = [10, 15, 12, 8, 11, 14, 13]

# Crear gráfico
fig, ax = plt.subplots()
ax.plot(precios)

# Configurar etiquetas
ax.set_title('Historial de precios')
ax.set_xlabel('Día')
ax.set_ylabel('Precio')

# Convertir a representación HTML interactiva
html = mpld3.fig_to_html(fig)

# Guardar en archivo HTML
with open('grafico.html', 'w') as f:
    f.write(html)

       