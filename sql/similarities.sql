CREATE DATABASE movielens;
USE movielens;

CREATE TABLE movies (
  PRIMARY KEY (id),
  id     INT NOT NULL,
  title  VARCHAR(100) NOT NULL
);

CREATE TABLE similarities (
  PRIMARY KEY (movie_id_from, movie_id_to),
  FOREIGN KEY (movie_id_from) REFERENCES movies(id),
  FOREIGN KEY (movie_id_to) REFERENCES movies(id),
  movie_id_from  INT NOT NULL,
  movie_id_to  INT NOT NULL,
  similarity  FLOAT NOT NULL
);

-- This table will be used for searching movie id by normalized title. Assume that movies titles are unique
CREATE TABLE normalized_movies (
  PRIMARY KEY (normalized_title),
  FOREIGN KEY (movie_id) REFERENCES movies(id),
  normalized_title  VARCHAR(100)  NOT NULL,
  movie_id          INT NOT NULL UNIQUE
);
