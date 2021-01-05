import datetime
import db

db.create_tables()


def prompt_add_movie():
    title = input("Movie Title: ")
    release_date = input("Release date (dd-mm-YYYY): ")
    parsed_date = datetime.datetime.strptime(release_date, "%d-%m-%Y")
    timestamp = parsed_date.timestamp()

    db.add_movie(title, timestamp)


def prompt_watch_movie():
    username = input("Who watched the movie?: ")
    title = input("Movie title: ")
    db.watch_movies(username, title)


def print_movies(header: str, movies: list):
    # Indexes
    TITLE = 0
    TIMESTAMP = 1

    print(f"--- {header} MOVIES ---")
    for movie in movies:
        movie_date = datetime.datetime.fromtimestamp(movie[TIMESTAMP])
        human_date = movie_date.strftime("%d-%b-%Y")
        print(f"{movie[TITLE]} (on {human_date})")
    print("---\n")


def print_watched_movies(username: str, movies: list):
    # Indexes
    TITLE = 1

    print(f"---{username.upper()} WATCHED MOVIE LIST---")
    for movie in movies:
        print(f"{movie[TITLE]}")
    print("---\n")


welcome = "WELCOME TO THE WATCHLIST APP\n\n"

menu = """Please select one of the following options:
1) Add new movie.
2) View upcoming movies.
3) View all movies.
4) Watch a movie.
5) View watched movies.
6) Exit.

Your selection: """

print(welcome)

while (user_input := input(menu)) != "6":
    if user_input == "1":
        prompt_add_movie()

    elif user_input == "2":
        movies = db.get_movies(upcoming=True)
        print_movies("UPCOMING", movies)

    elif user_input == "3":
        movies = db.get_movies(upcoming=False)
        print_movies("ALL", movies)

    elif user_input == "4":
        prompt_watch_movie()

    elif user_input == "5":
        username = input("Username: ")
        movies = db.get_watched_movies(username)
        print_watched_movies(username, movies)

    else:
        print("Invalid input, try again")
