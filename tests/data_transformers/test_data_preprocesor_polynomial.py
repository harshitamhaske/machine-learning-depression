import numpy as np
import pandas as pd
import inspect
from learner.data_transformers.data_preprocessor_polynomial import DataPreprocessorPolynomial
from rpy2.robjects import pandas2ri
import pytest


class TestDataPreprocessorPolynomial():
    @pytest.fixture()
    def subject(self):
        subject = DataPreprocessorPolynomial()
        return subject

    def test_process_adds_the_good_polynomials(self, subject):

        header = ['a', 'b', 'c']
        data = pd.DataFrame([[1, 2, 3], [3, 2, 1]], columns = header)
        result = subject.process(data)
        expected_length = 1 + 3 + 3 + 3
        expected_data_one = [
            1, 1, 2, 3, 1 * 1, 1 * 2, 1 * 3, 2 * 2, 2 * 3, 3 * 3
        ]
        expected_data_two = [
            1, 3, 2, 1, 3 * 3, 3 * 2, 3 * 1, 2 * 2, 2 * 1, 1 * 1
        ]
        assert np.shape(result)[0] == np.shape(data)[0]
        assert np.shape(result)[1] == expected_length
        assert np.array_equal(np.array(result[0:1])[0], expected_data_one)
        assert np.array_equal(np.array(result[1:2])[0], expected_data_two)

    def test_process_takes_into_account_the_degree(self, subject):
        data = [[1, 2, 3]]
        header = ['a', 'b', 'c']
        data = pd.DataFrame(data, columns = header)

        result = subject.process(data, degree=1)
        expected_data_deg1 = [1, 1, 2, 3]
        assert np.shape(result)[1] == len(expected_data_deg1)
        assert np.array_equal(np.array(result[0:1])[0], expected_data_deg1)

        result = subject.process(data, degree=2)
        expected_data_deg2 = [
            1, 1, 2, 3, 1 * 1, 1 * 2, 1 * 3, 2 * 2, 2 * 3, 3 * 3
        ]
        assert np.shape(result)[1] == len(expected_data_deg2)
        assert np.array_equal(np.array(result[0:1])[0], expected_data_deg2)

        result = subject.process(data, degree=3)
        # 1, 1, 2, 3, 1*1, 1*2, 1*3,  2*2, 2*3, 3*3,
        # 1*1*1, 1*1*2, 1*1*3, 1*2*2, 1*2*3, 1*3*3,
        # 2*2*2,
        # 3*2*2, 3*2*3, 3*3*3
        expected_data_deg3 = [
            1, 1, 2, 3, 1 * 1, 1 * 2, 1 * 3, 2 * 2, 2 * 3, 3 * 3, 1 * 1 * 1,
            1 * 1 * 2, 1 * 1 * 3, 1 * 2 * 2, 1 * 2 * 3, 1 * 3 * 3, 2 * 2 * 2,
            3 * 2 * 2, 3 * 2 * 3, 3 * 3 * 3
        ]

        assert np.shape(result)[1] == len(expected_data_deg3)
        assert np.array_equal(np.array(result[0:1])[0], expected_data_deg3)
