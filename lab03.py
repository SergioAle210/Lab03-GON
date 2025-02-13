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

    def crear_nodo(self, label, propiedades):

        query = f"CREATE (n:{label} {{ {', '.join([f'{k}: ${k}' for k in propiedades.keys()])} }})"
        
        with self.driver.session() as session:
            session.run(query, **propiedades)

    def crear_relacion(self, label1, prop1, relacion, label2, prop2, propiedades={}):
        
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

# PARA CREAR UN NODO SE HACE DE LA SIGUIENTE MANERA:
# LISTADO_DEL_NODO = [
#   {"PROPIEDAD": "DATO", "PROPIEDAD": "DATO"},
#   {"PROPIEDAD": "DATO", "PROPIEDAD": "DATO"},
#   {"PROPIEDAD": "DATO", "PROPIEDAD": "DATO"},
#   {"PROPIEDAD": "DATO", "PROPIEDAD": "DATO"}
# ]

# ITERAMOS PARA CADA DATO A INGRESAR
# for DATO in NODO
#   graph.crear_nodo("NODO", LISTADO_DEL_NODO) 


# Agregar 5 usuarios
usuarios = [
    {"name": "Carlos", "userId": 1},
    {"name": "Sergio", "userId": 2},
    {"name": "Brandon", "userId": 3},
    {"name": "Alejandro", "userId": 4},
    {"name": "Alberto", "userId": 5}
]

for usuario in usuarios:
    graph.crear_nodo("User", usuario)

# Agregar 5 películas
peliculas = [
    {"title": "¿Qué pasó ayer?", "movieId": 101, "year": 2009, "plot": "Un grupo de amigos despierta después de una despedida de soltero sin recordar nada y debe encontrar al novio desaparecido."},
    {"title": "Supercool", "movieId": 102, "year": 2007, "plot": "Dos amigos intentan comprar alcohol para una fiesta en su última noche antes de graduarse."},
    {"title": "The Matrix", "movieId": 103, "year": 1999, "plot": "Un hacker descubre la verdad sobre su realidad y lucha contra un sistema opresor."},
    {"title": "Dos tontos en apuros", "movieId": 104, "year": 1994, "plot": "Dos amigos tontos emprenden un viaje para devolver un maletín lleno de dinero sin saber que pertenece a criminales."},
    {"title": "Proyecto X", "movieId": 105, "year": 2004, "plot": "Un grupo de adolescentes organiza una fiesta que rápidamente se sale de control, causando un caos masivo."}
]


for pelicula in peliculas:
    graph.crear_nodo("Movie", pelicula)

# Agregar relaciones de calificación (cada usuario califica al menos 2 películas)

# PARA CREAR UNA RELACIÓN ENTRE DOS NODOS SE HACE DE LA SIGUIENTE MANERA:
# LISTADO_DE_RELACIONES = [
#   {"PROP_1": VALOR, "PROP_2": VALOR, "REL_PROP": VALOR},
#   {"PROP_1": VALOR, "PROP_2": VALOR, "REL_PROP": VALOR},
#   {"PROP_1": VALOR, "PROP_2": VALOR, "REL_PROP": VALOR}
# ]

# ITERAMOS SOBRE CADA RELACIÓN QUE QUEREMOS CREAR
# for RELACION in LISTADO_DE_RELACIONES:
#   graph.crear_relacion(
#       "LABEL_1", {"CLAVE_UNICA": RELACION["PROP_1"]},  # Nodo origen (Ej: User, identificado por userId)
#       "TIPO_DE_RELACION",                              # Tipo de relación (Ej: "RATED", "ACTED_IN")
#       "LABEL_2", {"CLAVE_UNICA": RELACION["PROP_2"]},  # Nodo destino (Ej: Movie, identificado por movieId)
#       {"PROPIEDAD_REL": RELACION["REL_PROP"]}          # Propiedades opcionales de la relación (Ej: rating, timestamp)
#   )


calificaciones = [
    {"userId": 1, "movieId": 101, "rating": 5, "timestamp": 1700000000},  # Carlos -> ¿Qué pasó ayer?
    {"userId": 1, "movieId": 102, "rating": 4, "timestamp": 1700000010},  # Carlos -> Supercool
    {"userId": 2, "movieId": 103, "rating": 5, "timestamp": 1700000020},  # Sergio -> The Matrix
    {"userId": 2, "movieId": 104, "rating": 3, "timestamp": 1700000030},  # Sergio -> Dos tontos en apuros
    {"userId": 3, "movieId": 105, "rating": 4, "timestamp": 1700000040},  # Brandon -> Proyecto X
    {"userId": 3, "movieId": 101, "rating": 3, "timestamp": 1700000050},  # Brandon -> ¿Qué pasó ayer?
    {"userId": 4, "movieId": 102, "rating": 5, "timestamp": 1700000060},  # Alejandro -> Supercool
    {"userId": 4, "movieId": 103, "rating": 4, "timestamp": 1700000070},  # Alejandro -> The Matrix
    {"userId": 5, "movieId": 104, "rating": 5, "timestamp": 1700000080},  # Alberto -> Dos tontos en apuros
    {"userId": 5, "movieId": 105, "rating": 4, "timestamp": 1700000090}   # Alberto -> Proyecto X
]

for calificacion in calificaciones:
    graph.crear_relacion(
        "User", {"userId": calificacion["userId"]},
        "RATED",
        "Movie", {"movieId": calificacion["movieId"]},
        {"rating": calificacion["rating"], "timestamp": calificacion["timestamp"]}
    )


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