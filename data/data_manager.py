import os
import psycopg2
import psycopg2.extras
import urllib


def establish_connection(connection_data=None):
    """
    Create a database connection based on the :connection_data: parameter

    :connection_data: Connection string attributes

    :returns: psycopg2.connection
    """
    try:
        if connection_data is None:
            connection_data = get_connection_data()
          
            urllib.parse.uses_netloc.append('postgres')
            url = urllib.parse.urlparse(os.environ.get('DATABASE_URL'))
            conn = psycopg2.connect(
                database=url.path[1:],
                user=url.username,
                password=url.password,
                host=url.hostname,
                port=url.port
            )
            conn.autocommit = True
        
    except psycopg2.Error:
        if connection_data is None:
            connection_data = get_connection_data()
        try:
            connect_str = "dbname={} user={} host={} password={}".format(connection_data['dbname'],
                                                                         connection_data['user'],
                                                                         connection_data['host'],
                                                                         connection_data['password'])
            conn = psycopg2.connect(connect_str)
            conn.autocommit = True
        except psycopg2.DatabaseError as e:
            print("Cannot connect to database.")
            print(e)
        else:
            return conn


def get_connection_data(db_name=None):
    """
    Give back a properly formatted dictionary based on the environment variables values which are started
    with :MY__PSQL_: prefix

    :db_name: optional parameter. By default it uses the environment variable value.
    """
    if db_name is None:
        db_name = os.environ.get('MY_PSQL_DBNAME')

    return {
        'dbname': db_name,
        'user': os.environ.get('MY_PSQL_USER'),
        'host': os.environ.get('MY_PSQL_HOST'),
        'password': os.environ.get('MY_PSQL_PASSWORD')
    }


def execute_script_file(file_path):
    """
    Execute script file based on the given file path.
    Print the result of the execution to console.

    Example:
    > execute_script_file('db_schema/01_create_schema.sql')

    :file_path: Relative path of the file to be executed.
    """
    package_directory = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(package_directory, file_path)
    with open(full_path) as script_file:
        with establish_connection() as conn, \
                conn.cursor() as cursor:
            try:
                sql_to_run = script_file.read()
                cursor.execute(sql_to_run)
                print("{} script executed successsfully.".format(file_path))
            except Exception as ex:
                print("Execution of {} failed".format(file_path))
                print(ex.args)


def execute_select(statement, variables=None):

    """Execute SELECT statement optionally parameterized

    Example:
    > execute_select('SELECT %(title)s;', variables={'title': 'Codecool'})

    :statment: SELECT statement

    :variables:  optional parameter dict"""
    result_set = []
    conn = establish_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(statement, variables)
            result_set = cursor.fetchall()
    return result_set


def execute_dml_statement(statement, variables=None):
    """
    Execute data manipulation query statement (optionally parameterized)

    :statment: SQL statement

    :variables:  optional parameter dict"""
    result = None
    with establish_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(statement, variables)
            try:
                result = cursor.fetchone()
            except psycopg2.ProgrammingError as pe:
                pass
    return result


def top_rated_shows():
    statement = ("""SELECT title, year, runtime, string_agg(genres.name, ',') as genres, rating, trailer, homepage, poster, overview, shows.id FROM shows
                    LEFT JOIN show_genres ON shows.id = show_genres.show_id
                    LEFT JOIN Genres ON genres.id = show_genres.genre_id
                    WHERE shows.active = TRUE
                    GROUP BY title, year, runtime, rating, trailer, homepage, poster, overview, shows.id
                    ORDER BY rating DESC;""")
    rows = execute_select(statement)
    return rows


def reg_new_user(conn, name, email, username, password):
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("""INSERT INTO users (name, email, username, password) VALUES (%s, %s, %s, %s);""", (name, email, username, password))


def get_user_data(username):
    statement = ("""SELECT username, password FROM users WHERE username = %(username)s;""")
    variables = {'username': username}
    rows = execute_select(statement, variables)
    return rows


def detailed_info(show_id):
    statement = ("""SELECT shows.id, title, year, runtime, rating, trailer, homepage, poster, overview, string_agg(genres.name, ',') FROM shows
                    LEFT JOIN show_genres ON shows.id = show_genres.show_id
                    LEFT JOIN Genres ON genres.id = show_genres.genre_id
                    WHERE shows.id= %(show_id)s
                    GROUP BY shows.id, title, year, runtime, rating, trailer, homepage, poster, overview;""")
    variables = {'show_id': show_id}
    rows = execute_select(statement, variables)
    return rows


def youtube_link(conn, trailer, show_id):
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("""UPDATE shows SET trailer=%s WHERE id=%s;""", (trailer, show_id))


def season_list(show_id):
    statement = ("""SELECT seasons.id, seasons.title, seasons.overview, array_agg(episodes.title), show_id FROM seasons
                        LEFT JOIN episodes ON seasons.id = episodes.season_id
                        WHERE show_id = %(show_id)s
                        GROUP BY seasons.id, seasons.title, seasons.overview
                        ORDER BY seasons.id ASC;""")
    variables = {'show_id': show_id}
    rows = execute_select(statement, variables)
    return rows


def overview(overview, season_id):
    statement = ("""UPDATE seasons SET overview=%(overview)s WHERE id=%(season_id)s;""")
    variables = {'overview': overview, 'season_id': season_id}
    rows = execute_select(statement, variables)
    return rows


def delete(conn, show_id):
    cursor = conn.cursor()
    cursor.execute("""UPDATE shows SET active=FALSE WHERE id=%s;""", (show_id,))


def display_deleted_shows():
    statement = ("""SELECT id, title, overview, poster FROM shows WHERE active=FALSE
                    ORDER BY title ASC;""")
    rows = execute_select(statement)
    return rows

def restore(conn, show_id):
    cursor = conn.cursor()
    cursor.execute("""UPDATE shows SET active=TRUE WHERE id=%s;""", (show_id,))
