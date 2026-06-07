import pandas as pd
import sqlite3

RAW_DIR = "data/raw"
DB_PATH = "data/movielens.db"

def load_raw():
    movies = pd.read_csv(f"{RAW_DIR}/movies.csv")
    ratings = pd.read_csv(f"{RAW_DIR}/ratings.csv")
    return movies, ratings

def clean(movies, ratings):
    # Drop rows with missing values
    ratings = ratings.dropna(subset=["userId", "movieId", "rating"])
    movies = movies.dropna(subset=["title", "genres"])

    # Remove duplicates
    ratings = ratings.drop_duplicates(subset=["userId", "movieId"])

    # Convert timestamp to readable date
    ratings["date"] = pd.to_datetime(ratings["timestamp"], unit="s").dt.date

    # Explode genres: "Action|Comedy" -> two rows
    movies["genre"] = movies["genres"].str.split("|")
    movies_exploded = movies.explode("genre")

    print(f"Clean: {len(ratings)} ratings, {len(movies)} movies")
    return movies_exploded, ratings

def build_mart(movies, ratings):
    # Join movies with ratings
    df = ratings.merge(movies[["movieId", "title", "genre"]], on="movieId")

    # Avg rating per genre
    genre_stats = (
        df.groupby("genre")["rating"]
        .agg(avg_rating="mean", total_ratings="count")
        .reset_index()
        .round(2)
        .sort_values("avg_rating", ascending=False)
    )

    # Top 10 movies by avg rating (min 50 ratings)
    movie_stats = (
        df.groupby(["movieId", "title"])["rating"]
        .agg(avg_rating="mean", total_ratings="count")
        .reset_index()
    )
    top_movies = (
        movie_stats[movie_stats["total_ratings"] >= 50]
        .sort_values("avg_rating", ascending=False)
        .head(10)
        .round(2)
    )

    return genre_stats, top_movies

def load_to_db(movies, ratings, genre_stats, top_movies):
    conn = sqlite3.connect(DB_PATH)
    movies.to_sql("stg_movies", conn, if_exists="replace", index=False)
    ratings.to_sql("stg_ratings", conn, if_exists="replace", index=False)
    genre_stats.to_sql("mart_genre_stats", conn, if_exists="replace", index=False)
    top_movies.to_sql("mart_top_movies", conn, if_exists="replace", index=False)
    conn.close()
    print("Loaded to DB:", DB_PATH)

def run():
    movies_raw, ratings_raw = load_raw()
    movies, ratings = clean(movies_raw, ratings_raw)
    genre_stats, top_movies = build_mart(movies, ratings)
    load_to_db(movies, ratings, genre_stats, top_movies)

if __name__ == "__main__":
    run()
