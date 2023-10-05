from decouple import config

print(config("COLLECTION"))

print(config("DATABASE"))

print(config("MONGODB"))