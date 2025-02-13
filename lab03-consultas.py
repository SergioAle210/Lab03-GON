# Este apartado es para realizar consultas a la base de datos de Neo4j
from lab03 import MovieGraph
from config import PASSWORD, USERNAME, URI  # Importar credenciales

graph = MovieGraph(URI, USERNAME, PASSWORD)
# -------------------------- CONSULTAS --------------------------
# Buscar un usuario específico en la base de datos por su ID
print("Buscando usuario con ID 1:")
usuarios_encontrados = graph.encontrar_usuario(user_id=1)
for usuario in usuarios_encontrados:
    print(usuario)

# Buscar una película específica por su título
print("\nBuscando película '¿Qué pasó ayer?':")
peliculas_encontradas = graph.encontrar_pelicula(title="¿Qué pasó ayer?")
for pelicula in peliculas_encontradas:
    print(pelicula)

# Buscar la relación de calificación entre un usuario y una película
print("\nBuscando relación de rating entre Carlos (ID 1) y '¿Qué pasó ayer?' (ID 103):")
rating_encontrado = graph.encontrar_rating(1, 103)
for relacion in rating_encontrado:
    print(relacion) # Imprimir los datos de la relación de calificación encontrada
# Cerrar la conexión con la base de datos al finalizar las consultas
graph.close()
