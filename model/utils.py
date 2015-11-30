import re

BRACE_PATTERN = r' \([^)]*\)'
MOVIES_COLUMN_COUNT = 3


def reindex_movies(movies_path, scores_path, movies_path_out, scores_path_out):
    """
    Movie ids in movielens database have gaps. Reindexes movie ids with continuous index
    """
    movies_in = open(movies_path, 'r')
    movies_out = open(movies_path_out, 'w')
    movie_index = {}
    prev_id = 0

    movies_in.readline()    # skip header
    for line in movies_in:
        line_split = line.split(',')
        movie_id = int(line_split[0])

        prev_id += 1
        movie_index[movie_id] = prev_id

        split_count = len(line_split)
        if split_count == MOVIES_COLUMN_COUNT:
            movie_title = line_split[1]
        else:   # some movies have a comma in its title
            if line_split[1].startswith("\"") and line_split[split_count-2].endswith("\""):
                movie_title = ','.join(line_split[1:split_count-1])
            else:
                print("ERROR: Unsupported string in the file " + movies_path + " : " + line)
                continue

        movies_out.write(str(prev_id) + "," + movie_title + "\n")

    movies_in.close()
    movies_out.close()

    scores_in = open(scores_path, 'r')
    scores_out = open(scores_path_out, 'w')

    scores_in.readline()    # skip header
    for line in scores_in:
        line_split = line.split(',')
        user_id = int(line_split[0])
        movie_id = int(line_split[1])
        score = float(line_split[2])

        scores_out.write(str(user_id) + "," + str(movie_index[movie_id]) + "," + str(score) + "\n")

    scores_in.close()
    scores_out.close()


def normalize_title(movie_title):
    """
    Normalizes movie titles (removes year, "the", etc)
    """
    movie_title = movie_title.replace('\"', '')

    movie_title = re.sub(BRACE_PATTERN, '', movie_title)    # remove year from movie title
    movie_title = movie_title.lower()
    if movie_title.startswith("the "):
        movie_title = movie_title.replace("the ", '', 1)

    if movie_title.startswith("a "):
        movie_title = movie_title.replace("a ", '', 1)

    if movie_title.endswith(", the"):
        movie_title = movie_title[:-len(", the")]

    movie_title = movie_title.replace(" a ", '').replace(" the ", '')
    movie_title = movie_title.replace('&', 'and').replace(',', '').replace(' ', '')
    return movie_title
