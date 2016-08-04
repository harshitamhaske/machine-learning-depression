from machine_learning_models.machine_learning_model import MachineLearningModel

from sklearn.dummy import DummyClassifier


class DummyClassifierModel(MachineLearningModel):

    def __init__(self, x, y, x_names, y_names, verbosity, **kwargs):
        super().__init__(x, y, x_names, y_names, model_type='classification', **kwargs)
        self.skmodel = DummyClassifier(strategy='constant', constant=0)

class DummyRandomClassifierModel(MachineLearningModel):

    def __init__(self, x, y, x_names, y_names, verbosity, **kwargs):
        super().__init__(x, y, x_names, y_names, model_type='classification', **kwargs)
        self.skmodel = DummyClassifier(strategy='uniform')

