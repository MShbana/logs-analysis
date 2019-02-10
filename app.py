#! /usr/bin/env python3.6

import datetime
import psycopg2


# Select the most popular three articles of all time.
query1 = """SELECT title,views
            FROM title_name_id_views LIMIT 3"""

# Select the most popular authors of all time.
query2 = """SELECT name, SUM(views) AS sum
            FROM title_name_id_views
            GROUP BY name
            ORDER BY sum DESC"""

# Select the days with the greatest error rate (greater than 1%).
query3 = """
SELECT error_requests.day,
                (error_requests.errors::decimal / total_requests.requests)
            FROM error_requests JOIN total_requests
            ON error_requests.day = total_requests.day
            WHERE error_requests.errors > 0.01 * total_requests.requests"""


def connect(database_name="news"):
    """Connect to the news data base and return connection and cursor."""

    try:
        connection = psycopg2.connect(f"dbname={database_name}")
        cursor = connection.cursor()
        return connection, cursor

    except psycopg2.DatabaseError as e:
        print(f"Unable to connect!\n{e}")


def print_top_articles():
    """Select the most popular articles from the database and display them."""

    # Connect to the database.
    connection, cursor = connect()

    # Execute query 1 that selects the most popular articles.
    cursor.execute(query1)

    # Fetch the 3 articles from the database and store them to a list of tuples.
    # Each tuple contains one article and its total number of views.
    articles_views = cursor.fetchall()

    # Close the connection with the database.
    connection.close()

    # Iterate over the fetched list of tuples and
    # print each article name with its total number of views.
    for i, (title, views) in enumerate(articles_views, 1):
        print(f"\t{i}. {title:35} {views:10} views")


def print_top_authors():
    """Select the most popular authors from the database and display them."""

    # Connect to the database.
    connection, cursor = connect()

    # Execute query2 that selects the most popular authors.
    cursor.execute(query2)

    # Fetch the authors from the database and store them to a list of tuples.
    # Each tuple contains one author and their total number of views.
    authors_views = cursor.fetchall()

    # Close the connection with the database.
    connection.close()

    # Iterate over the fetched list of tuples and
    # print each author's name with their total number of views.
    for i, (author, views) in enumerate(authors_views, 1):
        print(f"\t{i}. {author:35} {views:10} views")


def print_top_error_rate_dates():
    """Select the days with the heighest error rate (greater than 1%) and display them."""

    # Connect to the database.
    connection, cursor = connect()

    # Execute query3 that selects the days with the most error rate.
    cursor.execute(query3)

    # Fetch the days from the database and store them to a list ot tuples.
    # Each tuple contains one day, its number of requests that led to errors
    # and its number of requests that led to successes.
    error_days = cursor.fetchall()

    # Close the connection with the database.
    connection.close()

    # Iterate over the fetched list of tuples and
    # print each day and error rate.
    for i, (day, error_rate) in enumerate(error_days, 1):
        # Covnert each fetched day from timestamp type into
        # a string type with a "month day, year" format
        day = f"{day:%B %d, %Y}"

        print(f"\t{i}. {day:35} {error_rate:9.2%} errors")

if __name__ == "__main__":
    print(f"\n Most Popular Articles of All Time:\n{'-'*38}")
    print_top_articles()
    print(f"\n Most Popular Authors of All Time:\n{'-'*37}")
    print_top_authors()
    print(f"\n More than 1% of requests led to an error on this/those day(s):\n{'-'*65}")
    print_top_error_rate_dates()
