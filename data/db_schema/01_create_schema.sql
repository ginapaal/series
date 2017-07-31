DROP TABLE IF EXISTS show_genres;
DROP TABLE IF EXISTS show_characters;
DROP TABLE IF EXISTS episodes;
DROP TABLE IF EXISTS genres;
DROP TABLE IF EXISTS actors;
DROP TABLE IF EXISTS seasons;
DROP TABLE IF EXISTS shows; 


CREATE TABLE shows (
    id character varying(50) PRIMARY KEY NOT NULL,
    title character varying(100) NOT NULL,
    year date NOT NULL,
    overview character varying(2000),
    runtime smallint,
    trailer character varying(200),
    homepage character varying(200),
    rating numeric
);


CREATE TABLE genres (
    id SERIAL PRIMARY KEY NOT NULL,
    name character varying(30) NOT NULL
);


CREATE TABLE actors (
    id SERIAL PRIMARY KEY NOT NULL,
    name character varying(100) NOT NULL,
    birthday date NOT NULL,
    death date,
    biography character varying(1000)
);


CREATE TABLE seasons (
    id SERIAL PRIMARY KEY NOT NULL,
    season_number smallint NOT NULL,
    title character varying(100),
    overview character varying(2000),
    show_id character varying(50) NOT NULL
);


CREATE TABLE show_genres (
    id SERIAL PRIMARY KEY NOT NULL,
    show_id character varying(50) NOT NULL,
    genre_id integer NOT NULL
);


CREATE TABLE show_characters (
    id SERIAL PRIMARY KEY NOT NULL,
    show_id character varying(50) NOT NULL,
    actor_id integer NOT NULL,
    character_name character varying(100) NOT NULL
);


CREATE TABLE episodes (
    id SERIAL PRIMARY KEY NOT NULL,
    title character varying(100) NOT NULL,
    episode_number smallint NOT NULL,
    overview character varying(1000),
    season_id integer NOT NULL
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY NOT NULL, 
    username character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    password character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
);


ALTER TABLE ONLY seasons
    ADD CONSTRAINT fk_seasons_show_id FOREIGN KEY (show_id) REFERENCES shows(id);


ALTER TABLE ONLY episodes
    ADD CONSTRAINT fk_episodes_season_id FOREIGN KEY (season_id) REFERENCES seasons(id);


ALTER TABLE ONLY show_characters
    ADD CONSTRAINT fk_show_characters_actor_id FOREIGN KEY (actor_id) REFERENCES actors(id);


ALTER TABLE ONLY show_characters
    ADD CONSTRAINT fk_show_characters_show_id FOREIGN KEY (show_id) REFERENCES shows(id);


ALTER TABLE ONLY show_genres
    ADD CONSTRAINT fk_show_genres_genre_id FOREIGN KEY (genre_id) REFERENCES genres(id);

ALTER TABLE ONLY show_genres
    ADD CONSTRAINT fk_show_genres_show_id FOREIGN KEY (show_id) REFERENCES shows(id);

