import os
import json
import random

class Team:

    def __init__(self, name, scores, auton_rate, repair_time = 0, current_status = 1.0):
        self.name = name
        self.scores = scores
        self.auton_rate = auton_rate
        self.repair_time = repair_time
        self.current_status = current_status
        self.last_match_time = None

    @classmethod
    def fromScoresetFile(cls, filename):
        with open(filename, 'r') as f:
            score_strings = f.readline().split(',')
            scores = [int(i) for i in score_strings]
            auton_rate = float(f.readline())
            name = os.path.splitext(os.path.basename(f.name))[0]
        return cls(name, scores, auton_rate)

    @classmethod
    def fromJSON(cls, filename):
        with open(filename, 'r') as f:
            json_obj = json.load(f)
        return cls(json_obj['name'], json_obj['scores'], json_obj['auton_rate'], json_obj['repair_time'], json_obj['current_status'])

    def exportJSON(self):
        with open('team_data/' + self.name + '.json', 'w') as f:
            json.dump(self.__dict__, f)

    def give_score(self):
        raw_score = random.choice(self.scores)
        self.scores.remove(raw_score)
        self.exportJSON()
        return int(round(raw_score * self.current_status))
        
