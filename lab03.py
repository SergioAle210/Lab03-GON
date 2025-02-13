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

    def create_user(self, name, user_id):
        query = """
        CREATE (:User {name: $name, userId: $user_id})
        """
        with self.driver.session() as session:
            session.run(query, name=name, user_id=user_id)

    def create_movie(self, title, movie_id, year, plot):
        query = """
        CREATE (:Movie {title: $title, movieId: $movie_id, year: $year, plot: $plot})
        """
        with self.driver.session() as session:
            session.run(query, title=title, movie_id=movie_id, year=year, plot=plot)

    def create_rating(self, user_id, movie_id, rating, timestamp):
        query = """
        MATCH (u:User {userId: $user_id}), (m:Movie {movieId: $movie_id})
        CREATE (u)-[:RATED {rating: $rating, timestamp: $timestamp}]->(m)
        """
        with self.driver.session() as session:
            session.run(query, user_id=user_id, movie_id=movie_id, rating=rating, timestamp=timestamp)


# Configurar conexión con Neo4j desde config.py
graph = MovieGraph(config.NEO4J_URI, config.NEO4J_USER, config.NEO4J_PASSWORD)

# Ingresar datos a la base de datos.
graph.create_user("Carlos", 1)
graph.create_movie("Proyecto X", 101, 2012, "Un grupo de adolescentes organiza una fiesta que rápidamente se sale de control, causando un caos masivo.")
graph.create_rating(1, 101, 5, 1700000000)
print("Ejecutado exitosamente.")

# Cerrar conexión
graph.close()