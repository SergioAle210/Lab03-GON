Laboratorio 3 - Bases de datos 2

Este proyecto permite gestionar y consultar una base de datos de películas y usuarios utilizando **Neo4j**. Se incluyen funciones para crear nodos, relaciones y realizar consultas en la base de datos.

## 📌 Requisitos

Antes de ejecutar el proyecto, asegúrate de tener instalado lo siguiente:

1. **Python 3.x**

2. **Librerías necesarias** (puedes instalarlas con el siguiente comando):

```sh
pip install neo4j
```

3. **Un servidor de Neo4j en ejecución**, con las credenciales de acceso configuradas.

## 📂 Configuración

Antes de ejecutar el proyecto, necesitas crear un archivo `config.py` en la raíz del proyecto con la siguiente información:

```python
# config.py
USERNAME = "tu_usuario"
PASSWORD = "tu_contraseña"
URI = "bolt://localhost:7687"  # Cambia esto según la configuración de tu servidor Neo4j
```

## 🚀 Uso del Proyecto

### 1️⃣ Poblar la Base de Datos

Ejecuta `lab03.py` para insertar los datos iniciales en Neo4j:

```sh
python lab03.py
```

Este script creará nodos y relaciones en la base de datos de Neo4j.

### 2️⃣ Ejecutar Consultas

Después de poblar la base de datos, puedes ejecutar `lab03_consultas.py` para realizar consultas:

```sh
python lab03_consultas.py
```

## 🔧 Funcionalidades y Explicación de Métodos

### 🔹 `MovieGraph`

Esta clase maneja la conexión y operaciones con la base de datos Neo4j.

#### 📌 `__init__(self, uri, user, password)`

- Inicializa la conexión con Neo4j.
- **Parámetros:**
  - `uri` (str): URI del servidor Neo4j.
  - `user` (str): Nombre de usuario.
  - `password` (str): Contraseña.

#### 📌 `close(self)`

- Cierra la conexión con la base de datos.

#### 📌 `crear_nodo(self, label, propiedades)`

- Crea un nodo en la base de datos.
- **Parámetros:**
  - `label` (str): Tipo de nodo (ej. "Actor", "Movie").
  - `propiedades` (dict): Propiedades del nodo (ej. `{ "name": "Leonardo DiCaprio" }`).

#### 📌 `crear_relacion(self, label1, prop1, relacion, label2, prop2, propiedades={})`

- Crea una relación entre dos nodos.
- **Parámetros:**
  - `label1` (str): Tipo del primer nodo.
  - `prop1` (dict): Propiedades para identificar el primer nodo.
  - `relacion` (str): Tipo de relación (ej. "ACTED_IN").
  - `label2` (str): Tipo del segundo nodo.
  - `prop2` (dict): Propiedades para identificar el segundo nodo.
  - `propiedades` (dict, opcional): Propiedades de la relación.

#### 📌 `encontrar_usuario(self, user_id=None, name=None)`

- Busca un usuario por ID o nombre.
- **Parámetros:**
  - `user_id` (int, opcional): ID del usuario.
  - `name` (str, opcional): Nombre del usuario.
- **Retorna:**
  - Lista de usuarios encontrados.

#### 📌 `encontrar_pelicula(self, movie_id=None, title=None)`

- Busca una película por ID o título.
- **Parámetros:**
  - `movie_id` (int, opcional): ID de la película.
  - `title` (str, opcional): Título de la película.
- **Retorna:**
  - Lista de películas encontradas.

#### 📌 `encontrar_rating(self, user_id, movie_id)`

- Busca la relación "RATED" entre un usuario y una película.
- **Parámetros:**
  - `user_id` (int): ID del usuario.
  - `movie_id` (int): ID de la película.
- **Retorna:**
  - Diccionario con información del usuario, la relación y la película.

## 📄 Notas Adicionales

- Asegúrate de que Neo4j esté corriendo antes de ejecutar los scripts.
- Puedes modificar `lab03.py` para agregar más datos si es necesario.

---

¡Listo! Ahora puedes utilizar este proyecto para explorar y analizar datos de películas en Neo4j. 🎬🚀
