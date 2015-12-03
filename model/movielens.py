import sys
from configparser import ConfigParser
from svd import SVD
from similarities_dao import SimilaritiesDao
from dataset_utils import Utils


def main(movies_path, scores_path, db_config_path='../config.ini'):

    movies_reindexed_path = movies_path + "_reindexed"
    scores_reindexed_path = scores_path + "_reindexed"
    Utils.reindex_movies(movies_path, scores_path, movies_reindexed_path, scores_reindexed_path)

    f = open(scores_reindexed_path, 'r')

    scores = {}

    for line in f:
        line_split = line.split(',')
        user_id = int(line_split[0])
        movie_id = int(line_split[1])
        score = float(line_split[2])

        scores[user_id, movie_id] = score

    f.close()

    svd = SVD()
    svd.train(scores)
    similarities = svd.find_top_similar_items()

    db_config = ConfigParser()
    db_config.read(db_config_path)
    similarities_dao = SimilaritiesDao({"host": db_config.get("mysql", "host"), "user": db_config.get("mysql", "user"),
                                      "passwd": db_config.get("mysql", "passwd"), "db": db_config.get("mysql", "db")})

    movies = Utils.reindexed_movie_titles(movies_reindexed_path)
    normalized_movies = {}
    for (movie_id, title) in enumerate(movies):
        normalized_movies[Utils.normalize_title(title)] = movie_id

    similarities_dao.store_movies(movies)
    similarities_dao.store_normalized_movies(normalized_movies)
    similarities_dao.store_similarities(similarities)

    similarities_dao.close()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("ERROR: movielens takes two arguments: path to csv with movies and path to csv with scores")
    else:
        if sys.argv == 4:
            main(sys.argv[1], sys.argv[2], sys.argv[3])
        else:
            main(sys.argv[1], sys.argv[2])
