import MySQLdb


class SuggestionsDao:

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

    def store_suggestions(self, suggestions):
        # TODO: Possibly do batch insert
        query = "INSERT INTO suggestions(movie_title, similar_movies)" \
                "VALUES (%s, %s)"

        for (movie_title, similar_movies) in suggestions.items():
            self._cur.execute(query, (movie_title, similar_movies))

        self._db.commit()

    def close(self):
        self._cur.close()
        self._db.close()
