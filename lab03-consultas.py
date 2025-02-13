# Este apartado es para realizar consultas a la base de datos de Neo4j
from lab03 import MovieGraph
from config import PASSWORD, USERNAME, URI  # Importar credenciales

graph = MovieGraph(URI, USERNAME, PASSWORD)

print("Buscando usuario con ID 1:")
usuarios_encontrados = graph.encontrar_usuario(user_id=1)
for usuario in usuarios_encontrados:
    print(usuario)

print("\nBuscando película '¿Qué pasó ayer?':")
peliculas_encontradas = graph.encontrar_pelicula(title="¿Qué pasó ayer?")
for pelicula in peliculas_encontradas:
    print(pelicula)

print("\nBuscando relación de rating entre Carlos (ID 1) y '¿Qué pasó ayer?' (ID 103):")
rating_encontrado = graph.encontrar_rating(1, 103)
for relacion in rating_encontrado:
    print(relacion)

graph.close()
