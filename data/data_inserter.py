import requests
from data_manager import *
from init_db import *
import datetime
import os

headers = {
    'Content-Type': 'application/json',
    'trakt-api-version': '2',
    'trakt-api-key': os.environ.get('TRAKT_API_KEY')
}

trakt_api_url = 'https://api.trakt.tv'


def get_show_entity(show):
    show_entity = {
        'id': show['ids']['imdb'],
        'title': show['title'],
        'year': datetime.date(show['year'], 1, 1),
        'overview': show['overview'],
        'runtime': show['runtime'],
        'trailer': show['trailer'],
        'homepage': show['homepage'],
        'rating': show['rating']
    }
    return show_entity


def get_genre_ids(genre_list):
    genres = tuple((g.title() for g in genre_list))
    id_result = execute_select("SELECT id FROM genres WHERE name IN %s;", (genres,))
    genre_ids = [result[0] for result in id_result]
    return genre_ids


def insert_show_genres(genre_ids, show_entity):
    for genre_id in genre_ids:
        show_genre_statement = """INSERT INTO show_genres (show_id, genre_id) VALUES (%(show_id)s, %(genre_id)s);"""
        show_genre_param = {
            'show_id': show_entity['id'],
            'genre_id': genre_id
        }
        execute_dml_statement(show_genre_statement, show_genre_param)


def insert_shows(limit=20):
    url = trakt_api_url + '/shows/popular?limit={limit}&extended=full'.format(limit=limit)
    shows_request = requests.get(url, headers=headers)
    inserted_ids = []

    for show in shows_request.json():
        show_entity = get_show_entity(show)
        inserted_ids.append(show_entity['id'])

        statement = """INSERT INTO shows (id,
                                        title,
                                        year,
                                        overview,
                                        runtime,
                                        trailer,
                                        homepage,
                                        rating)
                                VALUES (%(id)s,
                                        %(title)s,
                                        %(year)s,
                                        %(overview)s,
                                        %(runtime)s,
                                        %(trailer)s,
                                        %(homepage)s,
                                        %(rating)s);"""
        execute_dml_statement(statement, show_entity)

        genre_ids = get_genre_ids(show['genres'])
        insert_show_genres(genre_ids, show_entity)

    return inserted_ids


def get_season_entity(season, show_id):
    season_entity = {
        'season_number': season['number'],
        'title': season['title'],
        'overview': season['overview'],
        'episode_count': season['episode_count'],
        'show_id': show_id
    }
    return season_entity


def get_season_id(show_id, season_number):
    stmt = """
        SELECT id
        FROM seasons
        WHERE show_id LIKE %(show_id)s
            AND season_number = %(season_number)s;
    """
    params = {
        'show_id': show_id + '%',
        'season_number': season_number
    }
    result = execute_select(stmt, params)
    return result[0][0]


def insert_episodes(show_id):
    url = trakt_api_url + '/shows/{show_id}/seasons?extended=episodes'.format(show_id=show_id)
    episode_request = requests.get(url, headers=headers)
    for season in episode_request.json():
        season_id = get_season_id(show_id, season['number'])
        for episode in season['episodes']:
            stmt = """
                INSERT INTO episodes (title, episode_number, season_id)
                SELECT COALESCE(%(title)s, '-'),
                    %(episode_number)s,
                    %(season_id)s;
            """
            params = {
                'title': episode['title'],
                'episode_number': episode['number'],
                'season_id': season_id
            }
            execute_dml_statement(stmt, params)


def insert_seasons(show_ids):
    show_seasons = {}
    for show_id in show_ids:
        url = trakt_api_url + '/shows/{show_id}/seasons?extended=full'.format(show_id=show_id)
        season_request = requests.get(url, headers=headers)
        for season in season_request.json():
            stmt = """INSERT INTO seasons (season_number,
                                            title,
                                            overview,
                                            show_id)
                                    VALUES (%(season_number)s,
                                            %(title)s,
                                            %(overview)s,
                                            %(show_id)s);"""

            season_entity = get_season_entity(season, show_id)
            execute_dml_statement(stmt, season_entity)
        insert_episodes(show_id)

    return show_seasons


def insert_genres():
    url = trakt_api_url + '/genres/movies'
    genre_request = requests.get(url, headers=headers)

    for genre in genre_request.json():
        statement = "INSERT INTO genres (name) VALUES (%(name)s);"
        execute_dml_statement(statement, {'name': genre['name']})


def main():
    init_db()
    create_schema()
    insert_genres()
    print("genres data inserted")
    inserted_show_ids = insert_shows(limit=20)
    print("show data inserted")
    show_seasons = insert_seasons(inserted_show_ids)
    print('season data inserted')

if __name__ == '__main__':
    main()
