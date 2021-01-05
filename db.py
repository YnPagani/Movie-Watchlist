import sqlite3
import datetime

# Queries ---------------------------------------------------------------------

CREATE_MOVIES_TABLE = "CREATE TABLE IF NOT EXISTS movies(title TEXT, " \
                      "release_timestamp REAL); "

CREATE_WATCHLIST_TABLE = "CREATE TABLE IF NOT EXISTS watched(watcher_name " \
                         "TEXT, title TEXT); "

INSERT_MOVIES = "INSERT INTO movies(title, release_timestamp) " \
                "VALUES (?,?);"

INSERT_WATCHED_MOVIE = "INSERT INTO watched(watcher_name, title) VALUES (?,?);"

DELETE_MOVIE = "DELETE FROM movies WHERE title = ?;"

SELECT_ALL_MOVIES = "SELECT * FROM movies;"

SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > ?;"

SELECT_WATCHED_MOVIES = "SELECT * FROM watched WHERE watcher_name = ?;"

SET_MOVIE_WATCHED = "UPDATE movies SET watched = 1 WHERE title = ?;"

# methods ---------------------------------------------------------------------

connection = sqlite3.connect("data.db")


def create_tables():
    with connection:
        connection.execute(CREATE_MOVIES_TABLE)
        connection.execute(CREATE_WATCHLIST_TABLE)


def add_movie(title: str, release_timestamp: float):
    with connection:
        connection.execute(INSERT_MOVIES, (title, release_timestamp))


def get_movies(upcoming: bool = False):
    with connection:
        cursor = connection.cursor()

        if upcoming:
            # Gets the timestamp since 1-Jan-1970 till this instant to compare
            # with the movie timestamp.
            today_timestamp = datetime.datetime.today().timestamp()
            cursor.execute(SELECT_UPCOMING_MOVIES, (today_timestamp,))
        else:
            cursor.execute(SELECT_ALL_MOVIES)

        return cursor.fetchall()


def watch_movies(username: str, title: str):
    with connection:
        connection.execute(DELETE_MOVIE, (title,))
        connection.execute(INSERT_WATCHED_MOVIE, (username, title))


def get_watched_movies(username: str):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_WATCHED_MOVIES, (username,))
        return cursor.fetchall()


def del_movie(title: str):
    with connection:
        connection.execute(DELETE_MOVIE, (title,))
