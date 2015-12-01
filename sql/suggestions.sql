CREATE DATABASE movielens;
USE movielens;


CREATE TABLE suggestions (
  PRIMARY KEY (movie_title),
  movie_title     VARCHAR(50)  NOT NULL,
  similar_movies  VARCHAR(500) NOT NULL
);
