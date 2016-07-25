import numpy as np
from data_output.std_logger import L
from mpi4py import MPI

class DistributedModelRunner:

    def __init__(self, models):
        L.info('Running distributed model runner')
        self.comm = MPI.COMM_WORLD
        self.size = self.comm.Get_size()
        self.rank = self.comm.Get_rank()
        L.info('This is node %d/%d' % (self.rank, self.size))
        self.models = models
        self.models = ['a', 'b','c','d','e']

    def fabricate_models(self, x, y, x_names, y_names, verbosity):
        L.info('Fabbing models')

        if (self.rank == 0):
            data = []
            for i in range(len(self.models)):
                if i == len(data):
                    data.append([])
                data[i].append(self.models[i])
        else:
            data = None

        self.comm.Barrier()

        if (self.rank == 0): L.info('Running %d models on %d nodes' % (len(data), self.size))
        if (self.rank == 0): L.info('Running ' + data)

        data = self.comm.scatter(data, root=0)

        for model in data[self.rank]:
            L.info('Training from MPI model runner on node %d' % self.rank)
            model = model(np.copy(x), np.copy(y), x_names, y_names, verbosity)
            model.train()

        self.comm.Barrier()

        if self.rank == 0: L.info('!!Trained all models!!')

        return self.comm.gather(data, root=0)


    def run_calculations(self, fabricated_models):

        if (self.rank == 0):
            data = []
            for i in range(len(fabricated_models)):
                if i == len(data):
                    data.append([])
                data[i].append(fabricated_models[i])
        else:
            data = None

        self.comm.Barrier()

        L.info(data)
        if (self.rank == 0): L.info('Running %d models on %d nodes' % (len(data), self.size))

        data = self.comm.scatter(data, root=0)

        L.info('Yes here! from %d' % self.rank)

        for model in data[self.rank]:
            L.info('Training from MPI model runner on node %d' % self.rank)
            model.train()
        self.comm.Barrier()

        if self.rank == 0: L.info('!!Trained all models!!')

        return self.comm.gather(data, root=0)
