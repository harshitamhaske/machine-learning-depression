# from sklearn.model_selection import GridSearchCV, ParameterGrid
# import os.path
# from queue import Queue
# from learner.data_output.std_logger import L
# from learner.machine_learning_models.grid_search_mine import GridSearchMine
# import random
# import math
# import numpy as np


# class DistributedGridSearch:

    # def __init__(self, ml_model, estimator, param_grid, cv, cpus_per_node=23):
        # # Number of nodes
        # self.comm = MPI.COMM_WORLD
        # self.size = self.comm.Get_size()
        # self.workers = self.size - 1
        # self.rank = self.comm.Get_rank()
        # self.cpus_per_node = cpus_per_node
        # self.skmodel = estimator
        # self.param_grid = ParameterGrid(param_grid)
        # self.cv = cv
        # self.ml_model = ml_model

    # def fit(self, X, y):
        # self.comm.Barrier()
        # if self.rank == 0:
            # L.info('\tStarting master')
            # return self.master()
        # else:
            # self.slave(X, y)
            # return False

    # def create_job_queue(self, shuffle, force_distribute=False):
        # queue = Queue()
        # shuffled_range = list(range(len(self.param_grid)))
        # if shuffle: random.shuffle(shuffled_range)

        # work_division = self.cpus_per_node

        # # If there are more workers than jobs, give each worker a small job. Otherwise just give them x number of jobs,
        # # according to the number of CPUs they have.
        # if self.cpus_per_node * self.workers > len(self.param_grid) and force_distribute:
            # work_division = math.ceil(len(self.param_grid) / self.workers)

        # temp = []
        # for job in shuffled_range:
            # temp.append(job)
            # if (len(temp) == work_division):
                # queue.put(temp)
                # temp = []

        # if len(temp) is not 0: queue.put(temp)

        # # Add an extra job for each node to stop at the end
        # for node in range(self.workers):
            # queue.put(StopIteration)

        # return queue

    # def write_output(self, qsize, wall_time, times):
        # file_name = ('exports/%s.csv' % self.ml_model.given_name)
        # if not os.path.isfile(file_name):
            # with open(file_name, "w") as output_file:
                # output_file.write(
                    # '"nodes", "cpus_per_node", "queue_size", "parameters", "cv", "wall_time", "average", "median", "standard_deviation"\n'
                # )

        # with open(file_name, "a") as output_file:
            # output = (self.size, self.cpus_per_node, qsize, len(self.param_grid), self.cv, wall_time, np.average(times),
                      # np.median(times), np.std(times))
            # output_file.write('%d,%d,%d,%d,%d,%0.2f,%0.2f,%0.2f,%0.2f\n' % output)

    # def master(self):
        # # Get the queue of jobs to create
        # queue = self.create_job_queue(shuffle=True, force_distribute=True)
        # qsize = queue.qsize()

        # status = MPI.Status()
        # # running_procs = set()
        # wt = MPI.Wtime()
        # L.info("\tMaster: Starting calculation of %d items, or %d parameters" % (qsize, len(self.param_grid)))
        # times = []
        # while not queue.empty():
            # obj = queue.get()
            # time = self.comm.recv(source=MPI.ANY_SOURCE, status=status)
            # self.comm.send(obj=obj, dest=status.Get_source())
            # L.info("\tMaster: Sending to node %d: %s (%d/%d)" % (status.Get_source(), obj, queue.qsize(), qsize))
            # if time >= 0:
                # times.append(time)
            # #L.info("\tMaster: Queue size: %d/%d (last job by node %d, %d number of configurations, %d nodes)" % (queue.qsize(), qsize, status.Get_source(),len(self.param_grid), self.workers))

        # wt = MPI.Wtime() - wt

        # L.info(
            # '\tQueue is empty, it contained %d items which took %0.2f seconds (%0.2f minutes). Avg: %0.2f, Median: %0.2f, Std: %0.2f'
            # % (qsize, wt, (wt / 60), np.average(times), np.median(times), np.std(times)))

        # self.write_output(qsize, wt, times)
        # models = []
        # models = self.comm.gather(models, root=0)
        # best_model = None
        # best_score = float('-inf')

        # L.info('\tWe received %d models' % len(models))
        # good_models = 0
        # for model in models:
            # if len(model) == 0: continue
            # for sub_model in model:
                # good_models += 1
                # if sub_model[0] > best_score:
                    # best_score = sub_model[0]
                    # best_model = sub_model[1]

        # L.info('\tThese models had %d good models' % (good_models))
        # L.info('\tThe score of the best model was %0.3f' % best_score)
        # return best_model

    # def slave(self, X, y):
        # models = []

        # my_X = np.copy(X)
        # my_y = np.copy(y)
        # run_time = 0
        # total_models = 0
        # last_run_time = -1
        # # Ask for work until we receive StopIteration
        # print('\t\tSlave %d: Started my new job, now waiting for data..' % self.rank)
        # for task in iter(lambda: self.comm.sendrecv(last_run_time, 0), StopIteration):
            # start = MPI.Wtime()
            # total_models += len(task)
            # grid = [self.param_grid[y] for y in task]
            # print('\t\tSlave %d: Received job: %s' % (self.rank, task))
            # model = GridSearchMine(
                # estimator=self.skmodel, param_grid=grid, n_jobs=-1, verbose=0, cv=self.cv).fit(
                    # X=my_X, y=my_y)
            # models.append((model.best_score_, model.best_estimator_))
            # last_run_time = MPI.Wtime() - start
            # print('\t\tSlave %d: finished calculation in %0.1f seconds' % (self.rank, last_run_time))
            # run_time += last_run_time
        # if total_models > 0:
            # print('\t\tSlave %d: took %0.0f seconds (avg %0.2f per model)' % (self.rank, run_time,
                                                                              # (run_time / total_models)))
        # else:
            # print('\t\tSlave %d: took %0.0f seconds' % (self.rank, run_time))
        # # Collective report to parent
        # self.comm.gather(sendobj=models, root=0)
