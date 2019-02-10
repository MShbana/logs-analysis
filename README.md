# Logs Analysis
First required project for the [Full Stack Web Developer Nanodegree][1].

## Project Overview

> In this project, you'll work with data that could have come from a real-world web application, with fields representing information that a web server would record, such as HTTP status codes and URL paths.

>You've been hired onto a team working on a newspaper site. The user-facing newspaper site front-end itself, and the database behind it, are already built and running. You've been asked to build an internal reporting tool that will use information from the database to discover what kind of articles the site's readers like.

>The database contains newspaper articles, as well as the web server log for the site. The log has a database row for each time a reader loaded a web page. Using that information, your code will answer questions about the site's user activity.

>The program you write in this project will run from the command line. It won't take any input from the user. Instead, it will connect to that database, use SQL queries to analyze the log data, and print out the answers to some questions.

>Your task is to create a reporting tool that prints out reports (in plain text) based on the data in the database. This reporting tool is a Python program using the psycopg2 module to connect to the database.

### The 3 questions the code should answer are:
1. What are the most popular three articles of all time?
2. Who are the most popular authors of all time?
3. On which days did more than 1% of requests lead to errors?
----
## Requirements
1. [VirtualBox][2]
2. [Vagrant][3].
3. Python3.6.x. (You'll need to update the Python version on the VM).
---
## Installation & Configuration
### Installing Linux Virtual Machine
1. Install VirtualBox.
2. Install vagrant.
3. To download the Virtual Machine Configuration, choose one of the following methods:
 * Download and unzip [Full-Stack-Nanodegree-Virtual-Machine.zip][4]
 * Fork and clone this [repository][5] from GitHub.

4. `cd` to the new directory and `cd` to **vagrant** subdiretory inside that directory.
5. `vagrant up` while inside the **vagrant** subdirectory on your host computer. This will download the Linux OS and install it as your VM.
6. When `vagrant up` is finished running, run `vagrant ssh` to launch the newly installed Linux VM.
7. You should see a shell prompt that looks like `vagrant@vagrant`. This means you are now logged in your new Linux VM.

### Running the Database
1. Run `vagrant up` to start your VM.
2. Run `vagrant ssh` to log into your VM.
3. Download the [data][6] and unzip the file.
4. The file inside is called `newsdata.sql`, move it into the `vagrant` subdirectory, which is shared with the VM.
5. `cd /vagrant` from inside your VM.
6. `psql -d news -f newsdata.sql` to load the **newspaper site's data** into your local database.

---

## How to Use
1. `psql -d news` to connect to the news database on your VM.

2. Create _**Views**_


- create the `title_name_id_views` view:

```sql
CREATE VIEW title_name_id_views AS
    SELECT articles.title, authors.name, authors.id, COUNT(*) AS views
        FROM log JOIN articles
            ON OVERLAY(log.path PLACING '' FROM 1 FOR 9) = articles.slug
        JOIN authors
            ON articles.author = authors.id
        GROUP BY articles.title, authors.name, authors.id
        ORDER BY views DESC;
```
This _view_ contains each article's title, their authors's names, authors' id's and number of views for each article.

`\d title_name_id_views`

| Column | Type |
| ------ | ---- |
| title | text |
| name | text |
| id | integer |
| views | bigint |

- create the `success_request` view:

```sql
CREATE VIEW total_requests AS
    SELECT time::timestamp::date AS day, COUNT(*) AS requests
        FROM log
        GROUP BY day
```
This _view_ contains all days and the number of successful requests in each day.

`\d success_request`

| Column | Type |
| ------ | ---- |
| day | date |
| count | bigint |

- create the `error_request` view:

```sql
CREATE VIEW error_requests AS
    SELECT time::timestamp::date AS day, COUNT(*) AS errors
        FROM log
        WHERE status != '200 OK'
        GROUP BY day
```
This _view_ contains all days and the number of requests that led to errors in each day.

`\d error_request`

| Column |Type |
| ------ | --- |
| day | date |
| count | bigint |


4. `python3 log-analysis.project` to run the program.

[//]:  # (Links and references)

[1]: <https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004>
[2]: <https://www.virtualbox.org/wiki/Download_Old_Builds_5_1>
[3]: <https://www.vagrantup.com/downloads.html>
[4]: <https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip>
[5]: <https://github.com/udacity/fullstack-nanodegree-vm>
[6]: <https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip>
