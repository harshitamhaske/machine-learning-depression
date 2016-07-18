from data_output.plotters.plotter import Plotter
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

import numpy as np


class ConfusionMatrixPlotter(Plotter):

    def plot(self, model, actual, predicted):
        if predicted is None or actual is None:
            return False


        cmap = plt.cm.Blues
        cmap = plt.cm.afmhot
        cmap = plt.cm.rainbow
        np.set_printoptions(precision=2)

        fig, ax = plt.subplots(1, 2, figsize=(15,15), dpi=72)

        tick_marks = np.arange(2)

        plt.setp(ax,xticks=tick_marks, xticklabels=['yes', 'no'],
                 yticks=tick_marks, yticklabels=['yes', 'no'])

        plot_name = model.given_name
        plot_name = 'confusion_matrix_' + plot_name.replace(" ", "_")
        print('\t -> Plotting ' + plot_name)

        cm = confusion_matrix(actual, predicted)

        print('\t --> True Positives: %d, True Negatives: %d, False Positives: %d, False Negatives: %d' % (
        cm[0, 0], cm[1, 1], cm[1, 0], cm[0, 1]))
        im = ax[0].imshow(cm, interpolation='nearest', cmap=cmap)

        ax[0].set_title('CFM:' + model.given_name)
        ax[0].set_ylabel('True label')
        ax[0].set_xlabel('Predicted label')
        fig.colorbar(im)

        cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print('\t -> Normalized ' + plot_name)
        print('\t --> True Positives: %d, True Negatives: %d, False Positives: %d, False Negatives: %d' % (
            cm_normalized[0, 0], cm_normalized[1, 1], cm_normalized[1, 0], cm_normalized[0, 1]))
        im = ax[1].imshow(cm_normalized, interpolation='nearest', cmap=cmap)
        ax[1].set_title('NCFM: ' + model.given_name)
        ax[1].set_ylabel('True label')
        ax[1].set_xlabel('Predicted label')


        fig.colorbar(im)
        fig.tight_layout()

        return self.return_file(plt, plot_name)