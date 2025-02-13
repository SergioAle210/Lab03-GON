# Sergio Orellana - 221122
# Brandon Reyes - 22992
# Carlos Valladares - 221164

from neo4j import GraphDatabase
import config 

class MovieGraph:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def usuarios(self, name, user_id):
        query = """
        CREATE (:User {name: $name, userId: $user_id})
        """
        with self.driver.session() as session:
            session.run(query, name=name, user_id=user_id)

    def peliculas(self, title, movie_id, year, plot):
        query = """
        CREATE (:Movie {title: $title, movieId: $movie_id, year: $year, plot: $plot})
        """
        with self.driver.session() as session:
            session.run(query, title=title, movie_id=movie_id, year=year, plot=plot)

    def ratings(self, user_id, movie_id, rating, timestamp):
        query = """
        MATCH (u:User {userId: $user_id}), (m:Movie {movieId: $movie_id})
        CREATE (u)-[:RATED {rating: $rating, timestamp: $timestamp}]->(m)
        """
        with self.driver.session() as session:
            session.run(query, user_id=user_id, movie_id=movie_id, rating=rating, timestamp=timestamp)


# Configurar conexión con Neo4j desde config.py
graph = MovieGraph(config.NEO4J_URI, config.NEO4J_USER, config.NEO4J_PASSWORD)

# Agregar 5 usuarios
usuarios = [
    {"name": "Carlos", "userId": 1},
    {"name": "Sergio", "userId": 2},
    {"name": "Brandon", "userId": 3},
    {"name": "Alejandro", "userId": 4},
    {"name": "Alberto", "userId": 5}
]

for usuario in usuarios:
    graph.usuarios(usuario["name"], usuario["userId"])

# Agregar 5 películas
peliculas = [
    {"title": "¿Qué pasó ayer?", "movieId": 101, "year": 2009, "plot": "Un grupo de amigos despierta después de una despedida de soltero sin recordar nada y debe encontrar al novio desaparecido."},
    {"title": "Supercool", "movieId": 102, "year": 2007, "plot": "Dos amigos intentan comprar alcohol para una fiesta en su última noche antes de graduarse."},
    {"title": "The Matrix", "movieId": 103, "year": 1999, "plot": "Un hacker descubre la verdad sobre su realidad y lucha contra un sistema opresor."},
    {"title": "Dos tontos en apuros", "movieId": 104, "year": 1994, "plot": "Dos amigos tontos emprenden un viaje para devolver un maletín lleno de dinero sin saber que pertenece a criminales."},
    {"title": "Proyecto X", "movieId": 105, "year": 2004, "plot": "Un grupo de adolescentes organiza una fiesta que rápidamente se sale de control, causando un caos masivo."}
]


for pelicula in peliculas:
    graph.peliculas(pelicula["title"], pelicula["movieId"], pelicula["year"], pelicula["plot"])

# Agregar relaciones de calificación (cada usuario califica al menos 2 películas)
calificaciones = [
    (1, 101, 5, 1700000000),  # Carlos -> ¿Qué pasó ayer?
    (1, 102, 4, 1700000010),  # Carlos -> Supercool
    (2, 103, 5, 1700000020),  # Sergio -> The Matrix
    (2, 104, 3, 1700000030),  # Sergio -> Dos tontos en apuros
    (3, 105, 4, 1700000040),  # Brandon -> Proyecto X
    (3, 101, 3, 1700000050),  # Brandon -> ¿Qué pasó ayer?
    (4, 102, 5, 1700000060),  # Alejandro -> Supercool
    (4, 103, 4, 1700000070),  # Alejandro -> The Matrix
    (5, 104, 5, 1700000080),  # Alberto -> Dos tontos en apuros
    (5, 105, 4, 1700000090)   # Alberto -> Proyecto X
]

for user_id, movie_id, rating, timestamp in calificaciones:
    graph.ratings(user_id, movie_id, rating, timestamp)

print("Ejecutado exitosamente.")

# Cerrar conexión
graph.close()