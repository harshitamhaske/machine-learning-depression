from data_transformers import output_data_cleaner, output_data_splitter
from dataInput import spss_reader
from dataOutput.csv_exporter import CsvExporter
from factories.questionnaire_factory import QuestionnaireFactory
from machineLearningModels import linear_regression_model, sync_model_runner, support_vector_machine_model, regression_tree_model
from models import participant
from models.questionnaires import IDSQuestionnaire, FourDKLQuestionnaire
from outputFileCreators.single_output_frame_creator import SingleOutputFrameCreator
import pickle
import numpy as np

from collections import deque


def create_participants(data):
    participants = {}
    for index, entry in data.iterrows():
        p = participant.Participant(entry['pident'], entry['Sexe'],
                                    entry['Age'])
        participants[p.pident] = p

    return participants


def read_cache(cache_name):
    with open(cache_name, 'rb') as input:
        header = pickle.load(input)
        data = pickle.load(input)
        return (header, data)


def write_cache(header, data, cache_name):
    with open(cache_name, 'wb') as output:
        pickle.dump(header, output, pickle.HIGHEST_PROTOCOL)
        pickle.dump(data, output, pickle.HIGHEST_PROTOCOL)


def print_header(header):
    print('Available headers:')
    for col in header:
        print('\t' + col)
    print()


if __name__ == '__main__':
    with_cache = True

    spss_reader = spss_reader.SpssReader()

    # First read demographic data
    N1_A100R = spss_reader.read_file("N1_A100R.sav")
    participants = create_participants(N1_A100R)

    single_output_frame_creator = SingleOutputFrameCreator()
    output_data_cleaner = output_data_cleaner.OutputDataCleaner()
    output_data_splitter = output_data_splitter.OutputDataSplitter()

    header, data = (None, None)
    print('Converting data to single dataframe...')
    if with_cache:
        header, data = read_cache('cache.pkl')
        print_header(header)
    else:
        questionnaires = QuestionnaireFactory.construct_questionnaires(
            spss_reader)
        data, header = (single_output_frame_creator.create_single_frame(
            questionnaires, participants))
        write_cache(header, data, 'cache.pkl')

    # Here we select the variables to use in the prediction. The format is:
    # AB-C:
    # - A = the time of the measurement, a = intake, c = followup
    # - B = the name of the questionnaire (check QuestionnaireFactory for the correct names)
    # - C = the name of the variable. Check the name used in the <Questionnairename>questionnaire.py
    X_NAMES = np.array(['pident', 'ademo-gender', 'ademo-age', 'aids-somScore',
                        'amasq-positiveAffectScore',
                        'amasq-negativeAffectScore', 'amasq-somatizationScore',
                        'abai-totalScore', 'abai-subjectiveScaleScore',
                        'abai-severityScore', 'abai-somaticScaleScore',
                        'a4dkl-somScore', 'a4dkl-severity',
                        'acidi-depression-majorDepressionLifetime',
                        'acidi-depression-dysthymiaLifetime',
                        'acidi-anxiety-socialfobiaInLifetime',
                        'acidi-anxiety-panicWithAgorafobiaInLifetime',
                        'acidi-anxiety-panicWithoutAgorafobiaInLifetime'])

    Y_NAMES = np.array(['cids-followup-somScore'])
    selected_header = np.append(X_NAMES, Y_NAMES)

    # Select the data we will use in the present experiment
    used_data = output_data_splitter.split(data, header, selected_header)

    # Determine which of this set are not complete
    incorrect_rows = output_data_cleaner.find_incomplete_rows(used_data)

    # Remove the incorrect cases
    used_data = output_data_cleaner.clean(used_data, incorrect_rows)

    # Split the dataframe into a x and y dataset.
    x_data = output_data_cleaner.clean(
        output_data_splitter.split(data, header, X_NAMES), incorrect_rows)
    y_data = output_data_cleaner.clean(
        output_data_splitter.split(data, header, Y_NAMES), incorrect_rows)

    # Convert ydata 2d matrix (x * 1) to 1d array (x)
    y_data = np.ravel(y_data)

    print(np.shape(x_data))
    print(np.shape(y_data))
    # Export all used data to a CSV file

    CsvExporter.export('../exports/merged_dataframe.csv', used_data,
                       selected_header)

    # Add the header to the numpy array, won't work now
    #data = map(lambda x: tuple(x), data)
    #data = np.array(deque(data), [(n, 'float64') for n in header])

    models = [
        linear_regression_model.LinearRegressionModel,
        support_vector_machine_model.SupportVectorMachineModel,
        regression_tree_model.RegressionTreeModel
    ]

    sync_model_runner = sync_model_runner.SyncModelRunner(models)
    result_queue = sync_model_runner.runCalculations(x_data, y_data, X_NAMES,
                                                     Y_NAMES)

    for i in range(0, result_queue.qsize()):
        model, prediction = result_queue.get()
        model.plot(model.y_train, prediction)
        model.print_accuracy()
