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
query3 = """SELECT error_request.day,
                error_request.count, success_request.count
            FROM error_request JOIN success_request
            ON error_request.day = success_request.day
            WHERE error_request.count >
                0.01*(success_request.count + error_request.count)"""


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
    for i, (title, view) in enumerate(articles_views, 1):
        print(f"\t{i}. {title:35} {view:10} views")


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
    for i, (author, view) in enumerate(authors_views, 1):
        print(f"\t{i}. {author:35} {view:10} views")


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

    # Convert fetched the error day(s) from timestamp into a string.
    error_date = str(error_days[0][0])

    # Round the error percentage to a two-decimal value.
    error_percent = round((error_days[0][1] /
                          (error_days[0][1] + error_days[0][2])) * 100, 2)
    error_date_formatted = datetime.datetime.strptime(error_date, "%Y-%m-%d")

    # Print the day and its error rate.
    print(f"\t{error_date_formatted.strftime('%b %d, %Y'):35} {error_percent:10}% errors")


if __name__ == "__main__":
    print(f"\n Most Popular Articles of All Time:\n{'-'*38}")
    print_top_articles()
    print(f"\n Most Popular Authors of All Time:\n{'-'*37}")
    print_top_authors()
    print(f"\n More than 1% of requests led to an error on this/those day(s):\n{'-'*65}")
    print_top_error_rate_dates()
