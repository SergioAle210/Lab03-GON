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




   # Encontrar un usuario por su ID o nombre
    def encontrar_usuario(self, user_id=None, name=None):
        query = """
        MATCH (u:User) 
        WHERE u.userId = $user_id OR u.name = $name
        RETURN u
        """
        with self.driver.session() as session:
            result = session.run(query, user_id=user_id, name=name)
            return [record["u"] for record in result]

    # Encontrar una película por ID o título
    def encontrar_pelicula(self, movie_id=None, title=None):
        query = """
        MATCH (m:Movie)
        WHERE m.movieId = $movie_id OR m.title = $title
        RETURN m
        """
        with self.driver.session() as session:
            result = session.run(query, movie_id=movie_id, title=title)
            return [record["m"] for record in result]

    # Encontrar un usuario y su relación RATED con una película
    def encontrar_rating(self, user_id, movie_id):
        query = """
        MATCH (u:User {userId: $user_id})-[r:RATED]->(m:Movie {movieId: $movie_id})
        RETURN u, r, m
        """
        with self.driver.session() as session:
            result = session.run(query, user_id=user_id, movie_id=movie_id)
            return [{"usuario": record["u"], "relacion": record["r"], "pelicula": record["m"]} for record in result]




# Configurar conexión con Neo4j desde config.py
graph = MovieGraph(config.NEO4J_URI, config.NEO4J_USER, config.NEO4J_PASSWORD)

# INICIO INCERSIÓN DE DATOS (SECCIÓN A COMENTAR PARA LAS CONSULTAS DE BÚSQUEDA PARA EVITAR ERRORES. EN CASO DE QUERER SOLO INSERTAR DATOS COMENTAR LA SECCIÓN DE CONSULTAS)

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

# FIN INCERCIÓN DE DATOS



# Inicio Funciones de búsqueda (¡IMPORTANTE!: PARA EJECUTAR ESTA PARTE COMENTAR LA INSERCIÓN DE DATOS ARRIBA PARA EVITAR ERRORES POR FAVOR)

print("Buscando usuario con ID 1:")
usuarios_encontrados = graph.encontrar_usuario(user_id=1)
for usuario in usuarios_encontrados:
    print(usuario)

print("\nBuscando película '¿Qué pasó ayer?':")
peliculas_encontradas = graph.encontrar_pelicula(title="¿Qué pasó ayer?")
for pelicula in peliculas_encontradas:
    print(pelicula)

print("\nBuscando relación de rating entre Carlos (ID 1) y '¿Qué pasó ayer?' (ID 101):")
rating_encontrado = graph.encontrar_rating(1, 101)
for relacion in rating_encontrado:
    print(relacion)

# Fin Funciones de búsqueda

print("Ejecutado exitosamente.")

# Cerrar conexión
graph.close()