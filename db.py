import os
import datetime
import psycopg2

from dotenv import load_dotenv

# Will make environment variables available for us
load_dotenv()

# Queries ---------------------------------------------------------------------
CREATE_USERS_TABLE = """CREATE TABLE IF NOT EXISTS users(
    username TEXT PRIMARY KEY
    );"""

CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS movies(
    id SERIAL PRIMARY KEY,
    title TEXT, 
    release_timestamp REAL
    );"""

CREATE_WATCHED_TABLE = """CREATE TABLE IF NOT EXISTS watched(
    user_username TEXT,
    movie_id INTEGER,
    FOREIGN KEY(user_username) REFERENCES users(username),
    FOREIGN KEY(movie_id) REFERENCES movies(id)
    );"""

INSERT_USER = "INSERT INTO users(username) VALUES (%s);"

INSERT_MOVIES = "INSERT INTO movies(title, release_timestamp) VALUES (%s, %s);"

INSERT_WATCHED_MOVIE = """INSERT INTO watched(user_username, movie_id) 
    VALUES (%s, %s);"""

DELETE_MOVIE = "DELETE FROM movies WHERE title = %s;"

SELECT_ALL_MOVIES = "SELECT * FROM movies;"

SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > %s;"

SEARCH_MOVIE = "SELECT * FROM movies WHERE title LIKE %s;"

SELECT_WATCHED_MOVIES = """SELECT movies.* 
    FROM movies 
    JOIN watched 
    ON movies.id = watched.movie_id
    JOIN users ON users.username = watched.user_username
    WHERE users.username = %s;"""


# methods ---------------------------------------------------------------------

connection = psycopg2.connect(os.environ["DATABASE_URL"])


def create_tables():
    with connection:
        with connection.cursor() as cursor:
            # Remember to always create tables with foreign keys after creating
            # the tables that those foreign keys refer to.
            cursor.execute(CREATE_USERS_TABLE)
            cursor.execute(CREATE_MOVIES_TABLE)
            cursor.execute(CREATE_WATCHED_TABLE)


def add_user(username: str):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_USER, (username,))


def add_movie(title: str, release_timestamp: float):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_MOVIES, (title, release_timestamp))


def del_movie(title: str):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(DELETE_MOVIE, (title,))


def watch_movies(username: str, movie_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_WATCHED_MOVIE, (username, movie_id))


def get_movies(upcoming: bool = False):
    with connection:
        with connection.cursor() as cursor:
            if upcoming:
                # Gets the timestamp since 1-Jan-1970 till this instant to
                # compare with the movie timestamp.
                today_timestamp = datetime.datetime.today().timestamp()
                cursor.execute(SELECT_UPCOMING_MOVIES, (today_timestamp,))
            else:
                cursor.execute(SELECT_ALL_MOVIES)

            return cursor.fetchall()


def get_watched_movies(username: str):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_WATCHED_MOVIES, (username,))
            return cursor.fetchall()


def search_movie(pattern: str):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SEARCH_MOVIE, (f"%{pattern}%",))
            return cursor.fetchall()
