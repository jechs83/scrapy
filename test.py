def generador_simple():
    yield 1
    yield 2
    yield 3

gen = generador_simple()

print(next(gen))  # Imprime 1
print(next(gen))  # Imprime 2
print(next(gen))  # Imprime 3
print(next(gen))  # Imprime 3