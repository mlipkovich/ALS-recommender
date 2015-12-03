import MySQLdb


class SimilaritiesDao:

    def __init__(self, db_config):
        """
        Connects to MySql database by given config
        :param db_config: dictionary with keys host, user, passwd and db
        """
        try:
            self._db = MySQLdb.connect(host=db_config["host"], user=db_config["user"],
                                       passwd=db_config["passwd"], db=db_config["db"])
            self._cur = self._db.cursor()
        except MySQLdb.Error as e:
            print("ERROR: Failed to connect to database with config " + db_config + "; reason: " + str(e))
            raise

    # TODO: Possibly do batch insert in all scripts
    def store_movies(self, movies):
        query = "INSERT INTO movies(id, title)" \
                "VALUES (%s, %s)"                   # Python string format doesn't work properly. Use %s for all types

        for (movie_id, title) in enumerate(movies):
            self._cur.execute(query, (movie_id, title))

        self._db.commit()

    def store_similarities(self, similarities):
        query = "INSERT INTO similarities(movie_id_from, movie_id_to, similarity)" \
                "VALUES (%s, %s, %s)"              # Python string format doesn't work properly. Use %s for all types

        for ((movie_id_from, movie_id_to), sim) in similarities.items():
            self._cur.execute(query, (movie_id_from, movie_id_to, sim))

        self._db.commit()

    def store_normalized_movies(self, normalized_movies):
        query = "INSERT INTO normalized_movies(normalized_title, movie_id)" \
                "VALUES (%s, %s)"                   # Python string format doesn't work properly. Use %s for all types

        for (normalized_title, movie_id) in normalized_movies.items():
            self._cur.execute(query, (normalized_title, movie_id))

        self._db.commit()

    def close(self):
        self._cur.close()
        self._db.close()
