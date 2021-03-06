import inspect

from learner.models.questionnaires.cidi_depression_derived import CIDIDepressionDerived
import pytest
import numpy as np


class TestCidiDepressionDerived:
    name = 'cidi_derived'
    filename = 'cidi.csv'
    measurement_moment = 'b'

    @pytest.fixture()
    def subject(self, mock_reader):
        subject = CIDIDepressionDerived(name=self.name,
                                        filename=self.filename,
                                        measurement_moment=self.measurement_moment,
                                        reader=mock_reader)
        return subject

    def test_init(self, subject):
        # Test if the super class is called with the correct parameters
        assert subject.name == self.name
        assert subject.filename == self.filename
        assert subject.measurement_moment == self.measurement_moment

    def test_correct_function_mapping(self, subject):
        result = subject.function_mapping
        assert result is not None

        # Test if all exported functions are defined
        all_functions = inspect.getmembers(subject, predicate=inspect.ismethod)
        all_functions = list(map(lambda function: function[1], all_functions))
        for funckey in result.keys():
            current = result[funckey]
            assert current in all_functions

    ##############
    # Depression #
    ##############
    @pytest.mark.parametrize('mock_get_field,expected', [
        ({'participant': 'participant',
          'field': 'cidep01',
          'value': 0}, 0),
        ({'participant': 'participant',
          'field': 'cidep01',
          'value': 1}, 1),
        ({'participant': 'participant',
          'field': 'cidep01',
          'value': -1}, np.nan),
    ],
                             indirect=True)
    def test_minor_depression_past_month(self, mock_get_field, expected, assert_with_nan, subject):
        assert_with_nan(subject.minor_depression_past_month('participant'), expected)

    @pytest.mark.parametrize('mock_get_field,expected', [
        ({'participant': 'participant',
          'field': 'cidep03',
          'value': 0}, 0),
        ({'participant': 'participant',
          'field': 'cidep03',
          'value': 1}, 1),
        ({'participant': 'participant',
          'field': 'cidep03',
          'value': -1}, np.nan),
    ],
                             indirect=True)
    def test_major_depression_past_month(self, mock_get_field, expected, assert_with_nan, subject):
        assert_with_nan(subject.major_depression_past_month('participant'), expected)

    @pytest.mark.parametrize('mock_get_field,expected', [
        ({'participant': 'participant',
          'field': 'cidep05',
          'value': 0}, 0),
        ({'participant': 'participant',
          'field': 'cidep05',
          'value': 1}, 1),
        ({'participant': 'participant',
          'field': 'cidep05',
          'value': -1}, np.nan),
    ],
                             indirect=True)
    def test_major_depression_past_six_months(self, mock_get_field, expected, assert_with_nan, subject):
        assert_with_nan(subject.major_depression_past_six_months('participant'), expected)

    @pytest.mark.parametrize('mock_get_field,expected', [
        ({'participant': 'participant',
          'field': 'cidep07',
          'value': 0}, 0),
        ({'participant': 'participant',
          'field': 'cidep07',
          'value': 1}, 1),
        ({'participant': 'participant',
          'field': 'cidep07',
          'value': -1}, np.nan),
    ],
                             indirect=True)
    def test_major_depression_past_year(self, mock_get_field, expected, assert_with_nan, subject):
        assert_with_nan(subject.major_depression_past_year('participant'), expected)

    @pytest.mark.parametrize('mock_get_field,expected', [
        ({'participant': 'participant',
          'field': 'cidep09',
          'value': 0}, 0),
        ({'participant': 'participant',
          'field': 'cidep09',
          'value': 1}, 1),
        ({'participant': 'participant',
          'field': 'cidep09',
          'value': -1}, np.nan),
    ],
                             indirect=True)
    def test_major_depression_lifetime(self, mock_get_field, expected, assert_with_nan, subject):
        assert_with_nan(subject.major_depression_lifetime('participant'), expected)

    ##############
    # Dysthymia #
    ##############
    @pytest.mark.parametrize('mock_get_field,expected', [
        ({'participant': 'participant',
          'field': 'cidep02',
          'value': 0}, 0),
        ({'participant': 'participant',
          'field': 'cidep02',
          'value': 1}, 1),
        ({'participant': 'participant',
          'field': 'cidep02',
          'value': -1}, np.nan),
    ],
                             indirect=True)
    def test_dysthymia_past_month(self, mock_get_field, expected, assert_with_nan, subject):
        assert_with_nan(subject.dysthymia_past_month('participant'), expected)

    @pytest.mark.parametrize('mock_get_field,expected', [
        ({'participant': 'participant',
          'field': 'cidep04',
          'value': 0}, 0),
        ({'participant': 'participant',
          'field': 'cidep04',
          'value': 1}, 1),
        ({'participant': 'participant',
          'field': 'cidep04',
          'value': -1}, np.nan),
    ],
                             indirect=True)
    def test_dysthymia_past_six_months(self, mock_get_field, expected, assert_with_nan, subject):
        assert_with_nan(subject.dysthymia_past_six_months('participant'), expected)

    @pytest.mark.parametrize('mock_get_field,expected', [
        ({'participant': 'participant',
          'field': 'cidep06',
          'value': 0}, 0),
        ({'participant': 'participant',
          'field': 'cidep06',
          'value': 1}, 1),
        ({'participant': 'participant',
          'field': 'cidep06',
          'value': -1}, np.nan),
    ],
                             indirect=True)
    def test_dysthymia_past_year(self, mock_get_field, expected, assert_with_nan, subject):
        assert_with_nan(subject.dysthymia_past_year('participant'), expected)

    @pytest.mark.parametrize('mock_get_field,expected', [
        ({'participant': 'participant',
          'field': 'cidep08',
          'value': 0}, 0),
        ({'participant': 'participant',
          'field': 'cidep08',
          'value': 1}, 1),
        ({'participant': 'participant',
          'field': 'cidep08',
          'value': -1}, np.nan),
    ],
                             indirect=True)
    def test_dysthymia_lifetime(self, mock_get_field, expected, assert_with_nan, subject):
        assert_with_nan(subject.dysthymia_lifetime('participant'), expected)

    ##########################################################
    # Number of current depression diagnoses (past 6 months) #
    ##########################################################
    @pytest.mark.parametrize('mock_get_field,expected', [
        ({'participant': 'participant',
          'field': 'cidep10',
          'value': 0}, 0),
        ({'participant': 'participant',
          'field': 'cidep10',
          'value': 1}, 1),
        ({'participant': 'participant',
          'field': 'cidep10',
          'value': -1}, np.nan),
    ],
                             indirect=True)
    def test_number_of_current_depression_diagnoses(self, mock_get_field, expected, assert_with_nan, subject):
        assert_with_nan(subject.number_of_current_depression_diagnoses('participant'), expected)

    @pytest.mark.parametrize('mock_get_field,expected', [
        ({'participant': 'participant',
          'field': 'cidep11',
          'value': 0}, 0),
        ({'participant': 'participant',
          'field': 'cidep11',
          'value': 1}, 1),
        ({'participant': 'participant',
          'field': 'cidep11',
          'value': -1}, np.nan),
    ],
                             indirect=True)
    def test_has_lifetime_depression_diagnoses(self, mock_get_field, expected, assert_with_nan, subject):
        assert_with_nan(subject.has_lifetime_depression_diagnoses('participant'), expected)

    @pytest.mark.parametrize('mock_get_field,expected', [
        ({'participant': 'participant',
          'field': 'cidep12',
          'value': 0}, 0),
        ({'participant': 'participant',
          'field': 'cidep12',
          'value': 1}, 1),
        ({'participant': 'participant',
          'field': 'cidep12',
          'value': -1}, np.nan),
    ],
                             indirect=True)
    def test_categories_for_lifetime_depression_diagnoses(self, mock_get_field, expected, assert_with_nan, subject):
        assert_with_nan(subject.categories_for_lifetime_depression_diagnoses('participant'), expected)

    @pytest.mark.parametrize('mock_get_field,expected', [
        ({'participant': 'participant',
          'field': 'cidep13',
          'value': 0}, 0),
        ({'participant': 'participant',
          'field': 'cidep13',
          'value': 1}, 1),
        ({'participant': 'participant',
          'field': 'cidep13',
          'value': -1}, np.nan),
    ],
                             indirect=True)
    def test_number_of_major_depression_episodes(self, mock_get_field, expected, assert_with_nan, subject):
        assert_with_nan(subject.number_of_major_depression_episodes('participant'), expected)

    @pytest.mark.parametrize('mock_get_field,expected', [
        ({'participant': 'participant',
          'field': 'cidep14',
          'value': 0}, 0),
        ({'participant': 'participant',
          'field': 'cidep14',
          'value': 1}, 1),
        # The expected value for -1 is 0 as -1 represents 'not having major depression'
        ({'participant': 'participant',
          'field': 'cidep14',
          'value': -1}, 0),
    ],
                             indirect=True)
    def test_major_depression_type(self, mock_get_field, expected, assert_with_nan, subject):
        assert_with_nan(subject.major_depression_type('participant'), expected)

