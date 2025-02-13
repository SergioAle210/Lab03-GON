# Sergio Orellana - 221122
# Brandon Reyes - 22992
# Carlos Valladares - 221164
# Importamos la librería para conectar con Neo4j
from neo4j import GraphDatabase
from config import PASSWORD, USERNAME, URI
from datetime import datetime

# Clase para manejar la conexión con Neo4j y realizar operaciones sobre el grafo
class MovieGraph:
    def __init__(self, uri, user, password):
        # Inicializa la conexión con Neo4j
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Cierra la conexión con Neo4j

        self.driver.close()
    
    def crear_nodo(self, label, propiedades):
        # Método para crear nodos en la base de datos
        #
        #Crea un nodo con una etiqueta y propiedades específicas en Neo4j.
        #:param label: Etiqueta del nodo (ej. "User", "Movie", "Actor").
        #:param propiedades: Diccionario con las propiedades del nodo.
        #
        # Genera la consulta Cypher para crear el nodo con las propiedades proporcionadas

        query = f"CREATE (n:{label} {{ {', '.join([f'{k}: ${k}' for k in propiedades.keys()])} }})"

        with self.driver.session() as session:
            session.run(query, **propiedades)

    def crear_relacion(self, label1, prop1, relacion, label2, prop2, propiedades={}):
        # Método para crear relaciones entre nodos en Neo4j

        query = f"""
        MATCH (a:{label1} {{{', '.join([f'{k}: ${'a_' + k}' for k in prop1.keys()])}}})
        MATCH (b:{label2} {{{', '.join([f'{k}: ${'b_' + k}' for k in prop2.keys()])}}})
        CREATE (a)-[:{relacion} {{{', '.join([f'{k}: ${'r_' + k}' for k in propiedades.keys()])}}}]->(b)
        """

        parametros = {f"a_{k}": v for k, v in prop1.items()}
        parametros.update({f"b_{k}": v for k, v in prop2.items()})
        parametros.update({f"r_{k}": v for k, v in propiedades.items()})

        with self.driver.session() as session:
            session.run(query, **parametros)

    # Encontrar un usuario por su ID o nombre
    def encontrar_usuario(self, user_id=None, name=None):
        #Busca un usuario en la base de datos por su ID o nombre.
        #:param user_id: ID del usuario.
        #:param name: Nombre del usuario.
        #:return: Lista de usuarios encontrados.
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
        #Busca una película en la base de datos por su ID o título.
        #:param movie_id: ID de la película.
        #:param title: Título de la película.
        #:return: Lista de películas encontradas.
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
        #Busca la relación de calificación entre un usuario y una película.
        #:param user_id: ID del usuario.
        #:param movie_id: ID de la película.
        #:return: Lista de relaciones de calificación
        query = """
        MATCH (u:User {userId: $user_id})-[r:RATED]->(m:Movie {movieId: $movie_id})
        RETURN u, r, m
        """
        with self.driver.session() as session:
            result = session.run(query, user_id=user_id, movie_id=movie_id)
            return [
                {
                    "usuario": record["u"],
                    "relacion": record["r"],
                    "pelicula": record["m"],
                }
                for record in result
            ]

# ------------------------------ EJECUCIÓN DEL PROGRAMA ------------------------------

# Crear una instancia de MovieGraph para conectar con Neo4j
# Configurar conexión con Neo4j desde config.py
graph = MovieGraph(URI, USERNAME, PASSWORD)

# Agregar 5 usuarios
usuarios = [
    {"name": "Carlos", "userId": 1},
    {"name": "Sergio", "userId": 2},
    {"name": "Brandon", "userId": 3},
    {"name": "Alejandro", "userId": 4},
    {"name": "Alberto", "userId": 5},
]

# Lista de actores
actores = [
    {
        "id": 1,
        "name": "Leonardo DiCaprio",
        "tmdbId": 6193,
        "born": datetime(1974, 11, 11),
        "died": None,
        "bornIn": "Los Angeles, USA",
        "url": "https://www.themoviedb.org/person/6193",
        "imdbId": 12345,
        "bio": "Actor ganador del Oscar.",
        "poster": "https://example.com/leonardo.jpg",
    },
    {
        "id": 2,
        "name": "Scarlett Johansson",
        "tmdbId": 1245,
        "born": datetime(1984, 11, 22),
        "died": None,
        "bornIn": "New York, USA",
        "url": "https://www.themoviedb.org/person/1245",
        "imdbId": 67890,
        "bio": "Actriz famosa por Black Widow.",
        "poster": "https://example.com/scarlett.jpg",
    },
    {
        "id": 3,
        "name": "Brad Pitt",
        "tmdbId": 287,
        "born": datetime(1963, 12, 18),
        "died": None,
        "bornIn": "Oklahoma, USA",
        "url": "https://www.themoviedb.org/person/287",
        "imdbId": 99988,
        "bio": "Actor conocido por Fight Club.",
        "poster": "https://example.com/bradpitt.jpg",
    },
    {
        "id": 4,
        "name": "Natalie Portman",
        "tmdbId": 524,
        "born": datetime(1981, 6, 9),
        "died": None,
        "bornIn": "Jerusalem, Israel",
        "url": "https://www.themoviedb.org/person/524",
        "imdbId": 77766,
        "bio": "Actriz de Black Swan y Star Wars.",
        "poster": "https://example.com/portman.jpg",
    },
    {
        "id": 5,
        "name": "Tom Hardy",
        "tmdbId": 2524,
        "born": datetime(1977, 9, 15),
        "died": None,
        "bornIn": "London, UK",
        "url": "https://www.themoviedb.org/person/2524",
        "imdbId": 55544,
        "bio": "Actor conocido por Mad Max y Venom.",
        "poster": "https://example.com/hardy.jpg",
    },
]

# Lista de directores
directores = [
    {
        "id": 6,
        "name": "Christopher Nolan",
        "tmdbId": 525,
        "born": datetime(1970, 7, 30),
        "died": None,
        "bornIn": "London, UK",
        "url": "https://www.themoviedb.org/person/525",
        "imdbId": 112233,
        "bio": "Director de Inception y The Dark Knight.",
        "poster": "https://example.com/nolan.jpg",
    },
    {
        "id": 7,
        "name": "Steven Spielberg",
        "tmdbId": 488,
        "born": datetime(1946, 12, 18),
        "died": None,
        "bornIn": "Ohio, USA",
        "url": "https://www.themoviedb.org/person/488",
        "imdbId": 334455,
        "bio": "Director de Jurassic Park y ET.",
        "poster": "https://example.com/spielberg.jpg",
    },
    {
        "id": 8,
        "name": "Quentin Tarantino",
        "tmdbId": 138,
        "born": datetime(1963, 3, 27),
        "died": None,
        "bornIn": "Tennessee, USA",
        "url": "https://www.themoviedb.org/person/138",
        "imdbId": 223344,
        "bio": "Director de Pulp Fiction y Kill Bill.",
        "poster": "https://example.com/tarantino.jpg",
    },
    {
        "id": 9,
        "name": "James Cameron",
        "tmdbId": 4,
        "born": datetime(1954, 8, 16),
        "died": None,
        "bornIn": "Ontario, Canada",
        "url": "https://www.themoviedb.org/person/4",
        "imdbId": 556677,
        "bio": "Director de Titanic y Avatar.",
        "poster": "https://example.com/cameron.jpg",
    },
    {
        "id": 10,
        "name": "Ridley Scott",
        "tmdbId": 578,
        "born": datetime(1937, 11, 30),
        "died": None,
        "bornIn": "England, UK",
        "url": "https://www.themoviedb.org/person/578",
        "imdbId": 889900,
        "bio": "Director de Alien y Gladiator.",
        "poster": "https://example.com/scott.jpg",
    },
]

# Lista de actores y directores
actoresydirectores = [
    {
        "id": 11,
        "name": "Clint Eastwood",
        "tmdbId": 1900,
        "born": datetime(1930, 5, 31),
        "died": None,
        "bornIn": "California, USA",
        "url": "https://www.themoviedb.org/person/1900",
        "imdbId": 667788,
        "bio": "Actor y director de cine legendario.",
        "poster": "https://example.com/eastwood.jpg",
    },
    {
        "id": 12,
        "name": "Ben Affleck",
        "tmdbId": 567,
        "born": datetime(1972, 8, 15),
        "died": None,
        "bornIn": "California, USA",
        "url": "https://www.themoviedb.org/person/567",
        "imdbId": 11223344,
        "bio": "Actor y director conocido por Argo.",
        "poster": "https://example.com/affleck.jpg",
    },
    {
        "id": 13,
        "name": "George Clooney",
        "tmdbId": 50,
        "born": datetime(1961, 5, 6),
        "died": None,
        "bornIn": "Kentucky, USA",
        "url": "https://www.themoviedb.org/person/50",
        "imdbId": 55443322,
        "bio": "Actor y director de cine.",
        "poster": "https://example.com/clooney.jpg",
    },
]


# Lista de películas
peliculas = [
    {
        "movieid": 101,
        "title": "Inception",
        "year": 2010,
        "tmdbld": 27205,
        "released": datetime(2010, 7, 16),
        "imdbRating": 8.8,
        "imdbId": 1375666,
        "runtime": 148,
        "countries": ["USA", "UK"],
        "imdbVotes": 2200000,
        "url": "https://www.themoviedb.org/movie/27205",
        "revenue": 829895144,
        "plot": "Un ladrón que entra en los sueños para robar secretos.",
        "poster": "https://example.com/inception.jpg",
        "budget": 160000000,
        "languagues": ["English", "Japanese"],
    },
    {
        "movieid": 102,
        "title": "Interstellar",
        "year": 2014,
        "tmdbld": 157336,
        "released": datetime(2014, 11, 7),
        "imdbRating": 8.6,
        "imdbId": 816692,
        "runtime": 169,
        "countries": ["USA", "Canada"],
        "imdbVotes": 1800000,
        "url": "https://www.themoviedb.org/movie/157336",
        "revenue": 677471339,
        "plot": "Los exploradores viajan a través de un agujero de gusano.",
        "poster": "https://example.com/interstellar.jpg",
        "budget": 165000000,
        "languagues": ["English"],
    },
    {
        "title": "¿Qué pasó ayer?",
        "movieId": 103,
        "year": 2009,
        "tmdbId": 12345,
        "released": datetime(2009, 6, 5),
        "imdbRating": 7.8,
        "imdbId": 987654,
        "runtime": 100,
        "countries": ["USA"],
        "imdbVotes": 1500000,
        "url": "https://www.themoviedb.org/movie/12345",
        "revenue": 467000000,
        "plot": "Un grupo de amigos despierta después de una despedida de soltero sin recordar nada y debe encontrar al novio desaparecido.",
        "poster": "https://example.com/hangover.jpg",
        "budget": 80000000,
        "languages": ["English", "Spanish"],
    },
    {
        "title": "Supercool",
        "movieId": 104,
        "year": 2007,
        "tmdbId": 8363,
        "released": datetime(2007, 8, 17),
        "imdbRating": 7.6,
        "imdbId": 477348,
        "runtime": 113,
        "countries": ["USA"],
        "imdbVotes": 800000,
        "url": "https://www.themoviedb.org/movie/8363",
        "revenue": 169800000,
        "plot": "Dos amigos intentan comprar alcohol para una fiesta en su última noche antes de graduarse.",
        "poster": "https://example.com/superbad.jpg",
        "budget": 20000000,
        "languages": ["English"],
    },
    {
        "title": "The Matrix",
        "movieId": 105,
        "year": 1999,
        "tmdbId": 603,
        "released": datetime(1999, 3, 31),
        "imdbRating": 8.7,
        "imdbId": 133093,
        "runtime": 136,
        "countries": ["USA", "Australia"],
        "imdbVotes": 1800000,
        "url": "https://www.themoviedb.org/movie/603",
        "revenue": 463517383,
        "plot": "Un hacker descubre la verdad sobre su realidad y lucha contra un sistema opresor.",
        "poster": "https://example.com/matrix.jpg",
        "budget": 63000000,
        "languages": ["English"],
    },
    {
        "title": "Dos tontos en apuros",
        "movieId": 106,
        "year": 1994,
        "tmdbId": 8467,
        "released": datetime(1994, 12, 16),
        "imdbRating": 7.3,
        "imdbId": 109105,
        "runtime": 107,
        "countries": ["USA"],
        "imdbVotes": 900000,
        "url": "https://www.themoviedb.org/movie/8467",
        "revenue": 247000000,
        "plot": "Dos amigos tontos emprenden un viaje para devolver un maletín lleno de dinero sin saber que pertenece a criminales.",
        "poster": "https://example.com/dumbanddumber.jpg",
        "budget": 17000000,
        "languages": ["English"],
    },
    {
        "title": "Proyecto X",
        "movieId": 107,
        "year": 2012,
        "tmdbId": 77016,
        "released": datetime(2012, 3, 2),
        "imdbRating": 6.6,
        "imdbId": 163682,
        "runtime": 88,
        "countries": ["USA"],
        "imdbVotes": 350000,
        "url": "https://www.themoviedb.org/movie/77016",
        "revenue": 102700000,
        "plot": "Un grupo de adolescentes organiza una fiesta que rápidamente se sale de control, causando un caos masivo.",
        "poster": "https://example.com/projectx.jpg",
        "budget": 12000000,
        "languages": ["English"],
    },
]


# Lista de géneros
generos = [
    {"name": "Action"},
    {"name": "Adventure"},
    {"name": "Comedy"},
    {"name": "Drama"},
    {"name": "Fantasy"},
    {"name": "Horror"},
    {"name": "Mystery"},
    {"name": "Romance"},
    {"name": "Sci-Fi"},
    {"name": "Thriller"},
]

calificaciones = [
    {
        "userId": 1,
        "movieId": 103,
        "rating": 5,
        "timestamp": 1700000000,
    },  # Carlos -> ¿Qué pasó ayer?
    {
        "userId": 1,
        "movieId": 102,
        "rating": 4,
        "timestamp": 1700000010,
    },  # Carlos -> Supercool
    {
        "userId": 2,
        "movieId": 103,
        "rating": 5,
        "timestamp": 1700000020,
    },  # Sergio -> The Matrix
    {
        "userId": 2,
        "movieId": 104,
        "rating": 3,
        "timestamp": 1700000030,
    },  # Sergio -> Dos tontos en apuros
    {
        "userId": 3,
        "movieId": 105,
        "rating": 4,
        "timestamp": 1700000040,
    },  # Brandon -> Proyecto X
    {
        "userId": 3,
        "movieId": 106,
        "rating": 3,
        "timestamp": 1700000050,
    },  # Brandon -> ¿Qué pasó ayer?
    {
        "userId": 4,
        "movieId": 102,
        "rating": 5,
        "timestamp": 1700000060,
    },  # Alejandro -> Supercool
    {
        "userId": 4,
        "movieId": 103,
        "rating": 4,
        "timestamp": 1700000070,
    },  # Alejandro -> The Matrix
    {
        "userId": 5,
        "movieId": 104,
        "rating": 5,
        "timestamp": 1700000080,
    },  # Alberto -> Dos tontos en apuros
    {
        "userId": 5,
        "movieId": 105,
        "rating": 4,
        "timestamp": 1700000090,
    },  # Alberto -> Proyecto X
]


actuaciones = [
    {"actorId": 1, "movieId": 101, "role": "Jack Dawson"},
    {"actorId": 2, "movieId": 102, "role": "Dominick Cobb"},
    {"actorId": 3, "movieId": 103, "role": "Tyler Durden"},
    {"actorId": 4, "movieId": 104, "role": "Mia Wallace"},
    {"actorId": 5, "movieId": 105, "role": "Bane"},
]

# Relaciones de dirección
direcciones = [
    {"directorId": 6, "movieId": 102, "role": "Director"},
    {"directorId": 7, "movieId": 103, "role": "Director"},
    {"directorId": 8, "movieId": 104, "role": "Director"},
    {"directorId": 9, "movieId": 101, "role": "Director"},
    {"directorId": 10, "movieId": 105, "role": "Director"},
]

# Actores que también son directores
actor_director = [
    {
        "id": 12,
        "movieId": 104,
        "acting_role": "Jules Winnfield",
        "directing_role": "Director",
    },
]

# Géneros de las películas

generos_peliculas = [
    {"movieId": 101, "genre": "Sci-Fi"},
    {"movieId": 102, "genre": "Romance"},
    {"movieId": 103, "genre": "Comedy"},
    {"movieId": 104, "genre": "Drama"},
    {"movieId": 105, "genre": "Fantasy"},
    {"movieId": 106, "genre": "Horror"},
    {"movieId": 107, "genre": "Mystery"},
]


def main():
    # Agregar usuarios
    for usuario in usuarios:
        graph.crear_nodo("User", usuario)
    # Agregar actores
    for actor in actores:
        graph.crear_nodo("Actor", actor)
    # Agregar directores
    for director in directores:
        graph.crear_nodo("Director", director)
    # Agregar actores y directores
    for actor in actoresydirectores:
        graph.crear_nodo("ActorDirector", actor)
    # Agregar películas
    for pelicula in peliculas:
        graph.crear_nodo("Movie", pelicula)
    # Agregar géneros
    for genero in generos:
        graph.crear_nodo("Genre", genero)
    # Agregar calificaciones
    for calificacion in calificaciones:
        graph.crear_relacion(
            "User",
            {"userId": calificacion["userId"]},
            "RATED",
            "Movie",
            {"movieId": calificacion["movieId"]},
            {"rating": calificacion["rating"], "timestamp": calificacion["timestamp"]},
        )
    # Agregar actuaciones
    for actuacion in actuaciones:
        graph.crear_relacion(
            "Actor",
            {"id": actuacion["actorId"]},
            "ACTED_IN",
            "Movie",
            {"movieId": actuacion["movieId"]},
            {"role": actuacion["role"]},
        )
    # Agregar direcciones
    for direccion in direcciones:
        graph.crear_relacion(
            "Director",
            {"id": direccion["directorId"]},
            "DIRECTED",
            "Movie",
            {"movieId": direccion["movieId"]},
            {"role": direccion["role"]},
        )
    # Agregar actores que también son directores
    for actor in actor_director:
        graph.crear_relacion(
            "ActorDirector",
            {"id": actor["id"]},
            "ACTED_IN",
            "Movie",
            {"movieId": actor["movieId"]},
            {"role": actor["acting_role"]},
        )
        graph.crear_relacion(
            "ActorDirector",
            {"id": actor["id"]},
            "DIRECTED",
            "Movie",
            {"movieId": actor["movieId"]},
            {"role": actor["directing_role"]},
        )
    # Agregar géneros de las películas
    for genero_pelicula in generos_peliculas:
        graph.crear_relacion(
            "Movie",
            {"movieId": genero_pelicula["movieId"]},
            "IN_GENRE",
            "Genre",
            {"name": genero_pelicula["genre"]},
        )


if __name__ == "__main__":
    # Sin de la inserción de datos
    main()

print("La inserción de datos fue exitosa.")

# Cerrar conexión
graph.close()
