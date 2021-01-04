import sqlite3
import datetime

# Queries ---------------------------------------------------------------------

CREATE_MOVIES_TABLE = "CREATE TABLE IF NOT EXISTS movies (title TEXT, " \
                      "release_timestamp REAL, watched INTEGER); "

INSERT_MOVIES = "INSERT INTO movies(title, release_timestamp, watched) " \
                "VALUES (?,?,0);"

SELECT_ALL_MOVIES = "SELECT * FROM movies;"

SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > ?;"

SELECT_WATCHED_MOVIES = "SELECT * FROM movies WHERE watched = 1;"

SET_MOVIE_WATCHED = "UPDATE movies SET watched = 1 WHERE title = ?;"

# methods ---------------------------------------------------------------------

connection = sqlite3.connect("data.db")


def create_tables():
    with connection:
        connection.execute(CREATE_MOVIES_TABLE)


def add_movie(title: str, release_timestamp: float):
    with connection:
        connection.execute(INSERT_MOVIES, (title, release_timestamp))


def get_movies(upcoming: bool = False):
    with connection:
        cursor = connection.cursor()

        if upcoming:
            # Gets the timestamp since 1-Jan- 1970 till this instant to compare
            # with the movie timestamp.
            today_timestamp = datetime.datetime.today().timestamp()
            cursor.execute(SELECT_UPCOMING_MOVIES, (today_timestamp,))
        else:
            cursor.execute(SELECT_ALL_MOVIES)

        return cursor.fetchall()


def watch_movies(title: str):
    with connection:
        connection.execute(SET_MOVIE_WATCHED, (title,))


def get_watched_movies():
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_WATCHED_MOVIES)
        return cursor.fetchall()
