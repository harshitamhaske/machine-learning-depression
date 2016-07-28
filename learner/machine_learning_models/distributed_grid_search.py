from sklearn.grid_search import GridSearchCV, ParameterGrid
from queue import Queue
from data_output.std_logger import L
from mpi4py import MPI
from machine_learning_models.grid_search_mine import GridSearchMine
import random


class DistributedGridSearch:

    def __init__(self, estimator, param_grid, cv):
        # Number of nodes
        self.comm = MPI.COMM_WORLD
        self.size = self.comm.Get_size()
        self.rank = self.comm.Get_rank()
        self.cpus_per_node = 12
        self.skmodel = estimator
        self.param_grid = ParameterGrid(param_grid)
        self.cv = cv

    def merge_dicts(self, dicts):
        result = {}
        for key in dicts[0].keys():
            result[key] = [d[key] for d in dicts]
        return result

    def fit(self, X, y):
        # Sync all nodes

        # self.comm.send(obj=1, dest=0)
        # if self.rank == 0:
        # a = 0
        # running = True
        # while (self.comm.recv() and running):
        # a += 1
        # print('%d of %d' % (a, self.size))
        # if a == self.size: running = False
        L.info('Approaching barrier')
        self.comm.Barrier()
        if self.rank == 0:
            L.info('\tStarting master')
            return self.master()

        else:
            L.info('\t\tStarting slave')
            self.slave(X, y)
            return False

    def create_job_queue(self, shuffle):
        queue = Queue()
        shuffled_range = list(range(len(self.param_grid)))
        if shuffle: random.shuffle(shuffled_range)

        temp = []
        for job in shuffled_range:
            if (job % self.cpus_per_node == 0 and job != 0) or (job == (len(self.param_grid) - 1)):
                if len(temp) is not 0: queue.put(temp)
                temp = []
            # current_job = self.merge_dicts([self.param_grid[job]])
            current_job = self.param_grid[job]
            temp.append(current_job)

        # Add an extra job for each node to stop at the end
        for node in range(self.size - 1):
            queue.put(StopIteration)

        return queue

    def master(self):

        # Get the queue of jobs to create
        queue = self.create_job_queue(shuffle=True)
        qsize = queue.qsize()

        status = MPI.Status()
        running_procs = set()
        wt = MPI.Wtime()
        while not queue.empty():
            recv = self.comm.recv(source=MPI.ANY_SOURCE, status=status)
            if recv == 'next':
                obj = queue.get()
                running_procs.add(status.Get_source())
                self.comm.send(obj=obj, dest=status.Get_source())
                # L.info("\t-------------------")
                # L.info("\tMaster: Sending to node %d: %s" % (status.Get_source(), obj))
                # L.info("\tMaster: Queue size: %d/%d (last job by node %d, %d number of configurations, %d/%d running nodes)" % (queue.qsize(), qsize, status.Get_source(),len(self.param_grid), len(running_procs), self.size))
                # L.info("\tMaster: %s nodes are still running" % running_procs)
                # L.info("\t-------------------")
            else:
                if status.Get_source() in running_procs: running_procs.remove(status.Get_source())

        wt = MPI.Wtime() - wt
        L.info(wt)
        L.info('\tQueue is empty, continueing')

        models = []
        models = self.comm.gather(models, root=0)
        best_model = None
        best_score = float('-inf')

        L.info('\tWe received %d models' % len(models))
        good_models = 0
        for model in models:
            if len(model) == 0: continue
            for sub_model in model:
                good_models += 1
                if sub_model[0] > best_score:
                    best_score = sub_model[0]
                    best_model = sub_model[1]

        L.info('\tThese models had %d good models' % (good_models))
        L.info('\tThe score of the best model was %0.3f' % best_score)
        return best_model

    def slave(self, X, y):
        models = []
        # Ask for work until we receive StopIteration
        # L.info('\t\tSlave: Waiting for data..')
        for task in iter(lambda: self.comm.sendrecv('next', 0), StopIteration):
            # L.info('\t\tSlave: Picking up a task on node %d, task size: %d' % (self.rank, len(task)))
            model = GridSearchMine(estimator=self.skmodel, param_grid=task, n_jobs=-1, verbose=0, cv=self.cv)
            model = model.fit(X=X, y=y)

            # only add the best model
            # L.info(model)
            model = (model.best_score_, model.best_estimator_)
            # L.info(model)

            # L.info('\t\t\t!!!!!!!!!! Appending model with score %f' % model[0])
            models.append(model)

        self.comm.send(obj='stop', dest=0)
        # Collective report to parent
        # L.info('\t\tFinished calculating (node %d), calculated %d models' % (self.rank, len(models)), force=True)
        self.comm.gather(sendobj=models, root=0)
        # L.info('\t\tByebye')
        #exit(0)