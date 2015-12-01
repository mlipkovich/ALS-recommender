import re


class Utils:

    BRACE_PATTERN = r' \([^)]*\)'

    def __init__(self):
        pass

    @staticmethod
    def reindex_movies(movies_path, scores_path, movies_path_out, scores_path_out, skip_header=True):
        """
        Movie ids in movielens database have gaps. Reindexes movie ids with continuous index.
        Reindex user ids to start from zero.
        """
        movies_in = open(movies_path, 'r')
        movies_out = open(movies_path_out, 'w')
        movie_index = {}
        prev_id = -1

        if skip_header:
            movies_in.readline()

        for line in movies_in:

            first_comma = line.find(',')
            last_comma = line.rfind(',')

            movie_id = int(line[:first_comma])
            movie_title = line[first_comma+1:last_comma]

            prev_id += 1
            movie_index[movie_id] = prev_id

            movies_out.write(str(prev_id) + "," + movie_title + "\n")

        movies_in.close()
        movies_out.close()

        scores_in = open(scores_path, 'r')
        scores_out = open(scores_path_out, 'w')

        if skip_header:
            scores_in.readline()

        for line in scores_in:
            line_split = line.split(',')
            user_id = int(line_split[0])
            movie_id = int(line_split[1])
            score = float(line_split[2])

            user_id -= 1    # start user ids from zero
            scores_out.write(str(user_id) + "," + str(movie_index[movie_id]) + "," + str(score) + "\n")

        scores_in.close()
        scores_out.close()

    @staticmethod
    def normalize_title(movie_title):
        """
        :return: Normalized movie title (removes year, "the", etc)
        """
        movie_title = movie_title.replace('\"', '')

        movie_title = re.sub(Utils.BRACE_PATTERN, '', movie_title)    # remove year from movie title
        movie_title = movie_title.lower()
        if movie_title.startswith("the "):
            movie_title = movie_title.replace("the ", '', 1)

        if movie_title.startswith("a "):
            movie_title = movie_title.replace("a ", '', 1)

        if movie_title.endswith(", the"):
            movie_title = movie_title[:-len(", the")]

        movie_title = movie_title.replace(" a ", ' ').replace(" the ", ' ')
        movie_title = movie_title.replace('&', "and").replace(',', '').replace(' ', '').replace('\n', '')
        return movie_title

    @staticmethod
    def reindexed_movie_titles(reindexed_movies_path):
        """
        :return: List of all movies titles
        """
        movies_in = open(reindexed_movies_path, 'r')
        movie_titles = []

        for line in movies_in:
            movie_title = line[line.find(',')+1:]
            movie_title = movie_title.replace('\n','')
            movie_titles.append(movie_title)
        movies_in.close()

        return movie_titles
