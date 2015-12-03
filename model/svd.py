import numpy as np


class SVD:

    def __init__(self):
        self._U, self._V = (np.empty(0), np.empty(0))
        self._user_bias, self._item_bias = (np.empty(0), np.empty(0))
        self._global_mean = 0
        self._scores = {}

        return

    @staticmethod
    def _predict(u, v, user_bias, item_bias, mean):
        return mean + user_bias + item_bias + np.dot(u, v)

    @staticmethod
    def _similarity(a, b):
        return np.dot(a, b)/np.sqrt(np.dot(a, a))/np.sqrt(np.dot(b, b))

    def _calculate_rmse(self):
        rmse = 0
        ratings_count = 0
        for ((user, item), rating) in self._scores.items():
            predicted_score = SVD._predict(self._U[:, user], self._V[:, item],
                                            self._user_bias[user], self._item_bias[item], self._global_mean)
            rmse += np.square(rating - predicted_score)
            ratings_count += 1

        rmse /= ratings_count
        return np.sqrt(rmse)

    def item_similarity(self, item_id_a, item_id_b):
        if item_id_a >= self._V.shape[1] or item_id_b >= self._V.shape[1]:
            print("ERROR: Max item id is " + str(self._V.shape[1]))
            return

        item_a = self._V[:, item_id_a]
        item_b = self._V[:, item_id_b]
        return SVD._similarity(item_a, item_b)

    def user_similarity(self, user_id_a, user_id_b):
        if user_id_a >= self._U.shape[1] or user_id_b >= self._U.shape[1]:
            print("ERROR: Max user id is " + str(self._U.shape[1] - 1))
            return

        user_a = self._U[:, user_id_a]
        user_b = self._U[:, user_id_b]

        return SVD._similarity(user_a, user_b)

    def find_top_similar_items(self, n_top=10):
        """
        For each item looks for n_top the most similar items
        :param n_top: number of similar items to look for for each item
        :return: map from (item 1, item 2) to their similarity
        """
        print("Calculate all item features norms for normalizing")
        v_norms = np.zeros(self._V.shape[1])
        for item_id, v in enumerate(self._V.T):
            v_norms[item_id] = np.sqrt(np.dot(v, v))

        print("Searching similar items")
        similarities = {}
        for item_id, v in enumerate(self._V.T):
            item_similarities = np.divide(np.dot(v, self._V), v_norms)/v_norms[item_id]
            item_similarities[item_id] = -np.inf  # for not returning element itself as the most similar
            top_indices = np.argpartition(item_similarities, -n_top)[-n_top:]
            for (similar_item_id, similarity) in zip(top_indices, item_similarities[top_indices]):
                similarities[item_id, similar_item_id] = similarity

        return similarities

    def train(self, scores, n_factor=100, max_iteration=2000, learning_rate=0.003, regularization=0.05, eps=1e-5):
        """
        Trains SVD model with user and item biases. Uses gradient descent with incremental learning approach
        :param scores: map (user id, item id) -> score
        """
        self._scores = scores

        # Need for arrays allocation
        max_user_id = 0
        max_item_id = 0
        for ((user_id, item_id), score) in self._scores.items():
            max_user_id = max(max_user_id, user_id)
            max_item_id = max(max_item_id, item_id)

        self._U = np.random.rand(n_factor, max_user_id + 1)
        self._V = np.random.rand(n_factor, max_item_id + 1)
        self._user_bias = np.random.rand(max_user_id + 1)
        self._item_bias = np.random.rand(max_item_id + 1)
        self._global_mean = np.random.rand()

        rmse_prev = np.inf
        rmse = self._calculate_rmse()
        n_iter = 0
        while (rmse_prev - rmse) > eps and n_iter < max_iteration:
            print("Starting iteration " + str(n_iter) + "; RMSE: " + str(rmse))

            for ((user_id, item_id), score) in self._scores.items():
                u = self._U[:, user_id]
                v = self._V[:, item_id]
                b_u = self._user_bias[user_id]
                b_i = self._item_bias[item_id]

                predicted_score = SVD._predict(u, v, b_u, b_i, self._global_mean)
                error = score - predicted_score

                k1 = 1-learning_rate*regularization
                k2 = learning_rate*error

                self._U[:, user_id] = k1 * u + k2 * v
                self._V[:, item_id] = k1 * v + k2 * u
                self._user_bias[user_id] = k1*b_u + k2
                self._item_bias[item_id] = k1*b_i + k2
                self._global_mean = k1*self._global_mean + k2

            rmse_prev = rmse
            rmse = self._calculate_rmse()
            n_iter += 1

        print("Training finished! Iterations count: " + str(n_iter) + "; RMSE: " + str(rmse))