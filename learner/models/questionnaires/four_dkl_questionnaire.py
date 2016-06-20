from models.questionnaire import Questionnaire


class FourDKLQuestionnaire(Questionnaire):

    def __init__(self, name, filename, measurement_moment, reader):
        function_mapping = {'somScore': self.somScore, 'severity': self.severity}

        super().__init__(name, filename, measurement_moment, reader, function_mapping)
        self.variables_for_som_score = [
            '4dkld01', '4dkld02', '4dkld03', '4dkld04', '4dkld05', '4dkld06', '4dkld07', '4dkld08', '4dkld09',
            '4dkld10', '4dkld11', '4dkld12', '4dkld13', '4dkld14', '4dkld15', '4dkld16'
        ]

    def somScore(self, participant):
        dat = self.getRow(participant)
        tot = 0
        for name in self.variables_for_som_score:
            q_name = self.variableName(name)
            if q_name in dat and dat[q_name] >= 0:
                tot += dat[q_name]

        return tot

    def severity(self, participant):
        score = self.somScore(participant)
        if score <= 13:
            return 0
        elif score <= 25:
            return 1
        elif score <= 38:
            return 2
        elif score <= 48:
            return 3
        elif score <= 84:
            return 4

        return None