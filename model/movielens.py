import sys
from configparser import ConfigParser
from svd import SVD
from suggestions_dao import SuggestionsDao
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
    suggestions = svd.find_top_similar_items()
    string_suggestions = {}

    movie_titles = Utils.reindexed_movie_titles(movies_reindexed_path)

    for (movie_id, similar_items) in enumerate(suggestions):
        movie_title = Utils.normalize_title(movie_titles[movie_id])
        string_suggestions[movie_title] = ';'.join(map(lambda x: movie_titles[x], similar_items))

    db_config = ConfigParser()
    db_config.read(db_config_path)
    suggestions_dao = SuggestionsDao({"host": db_config.get("mysql", "host"), "user": db_config.get("mysql", "user"),
                                      "passwd": db_config.get("mysql", "passwd"), "db": db_config.get("mysql", "db")})
    suggestions_dao.store_suggestions(string_suggestions)
    suggestions_dao.close()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("ERROR: movielens takes two arguments: path to csv with movies and path to csv with scores")
    else:
        if sys.argv == 4:
            main(sys.argv[1], sys.argv[2], sys.argv[3])
        else:
            main(sys.argv[1], sys.argv[2])
