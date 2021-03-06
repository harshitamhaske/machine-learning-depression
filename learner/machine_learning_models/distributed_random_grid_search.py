# from sklearn.model_selection import GridSearchCV, ParameterGrid, RandomizedSearchCV
# import os.path
# from queue import Queue
# from learner.data_output.std_logger import L
# from learner.machine_learning_models.grid_search_mine import GridSearchMine
# import random
# import math
# import numpy as np
# import time


# class DistributedRandomGridSearch:

    # def __init__(self, ml_model, estimator, param_grid, cv, n_iter=10000):
        # # Number of nodes
        # self.comm = MPI.COMM_WORLD
        # self.size = self.comm.Get_size()
        # self.rank = self.comm.Get_rank()
        # self.root = self.rank == 0
        # self.cpus_per_node = 23
        # self.skmodel = estimator
        # self.param_grid = param_grid
        # self.cv = cv
        # self.ml_model = ml_model
        # self.iterations = n_iter

    # def fit(self, X, y):
        # my_X = np.copy(X)
        # my_y = np.copy(y)

        # if (self.root):
            # # Create an array of elements with the number of jobs for each of the slaves
            # iterations = [round(self.iterations / self.size)] * self.size
        # else:
            # iterations = np.empty(self.size)

        # L.info('Running %d iterations on %d nodes.' % (iterations[0], self.size))
        # iterations = self.comm.scatter(iterations, root=0)

        # # Actual calculation
        # my_data = []
        # my_iterations = max(1, iterations)  #round(iterations / len(self.param_grid))
        # for param_grid in self.param_grid:
            # model = self.fit_single_model(my_X, my_y, param_grid, my_iterations)
            # my_data.append((model.best_score_, model.best_estimator_))

        # best_model_and_score = self.get_best_model(my_data)

        # self.comm.Barrier()

        # L.info('!!Trained all models!!')

        # best_model_and_score = self.comm.gather(best_model_and_score, root=0)

        # best_model = None
        # if self.root:
            # best_score, best_model = self.get_best_model(best_model_and_score)
            # L.info('\tThese models had %d good models' % (len(best_model_and_score)))
            # L.info('\tThe score of the best model was %0.3f' % best_score)

        # # Send the model to all clients
        # best_model = self.comm.bcast(best_model, root=0)
        # return best_model

    # def fit_single_model(self, X, y, param_grid, iterations):
        # """
        # Fits a single model using randomized gridsearch.
        # :param X: The x data to train the model on
        # :param y: the outcome data to train the model on
        # :param param_grid: the parameter grid to use for fitting the model
        # :param iterations: the number of iterations to use for the randomization (how many steps it should try)
        # :return: the fitted model.
        # """
        # model = RandomizedSearchCV(
            # estimator=self.skmodel, param_distributions=param_grid, n_jobs=-1, verbose=1, cv=self.cv, n_iter=iterations)
        # L.info('Here we go, node %d starts calculating %s' % (self.rank, self.ml_model.given_name), force=True)
        # model = model.fit(X=X, y=y)
        # return model

    # def get_best_model(self, models):
        # best_model = None
        # best_score = float('-inf')
        # L.info('\tWe received %d models' % len(models))
        # for model in models:
            # if (model is not None):
                # if model[0] > best_score:
                    # best_score = model[0]
                    # best_model = model[1]
        # return (best_score, best_model)
