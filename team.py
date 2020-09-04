import os
import json
import random
from datetime import datetime

class Team:

    def __init__(self, name, scores, auton_rate, repair_time = 0, robot_health = 1.0, last_match_time = None, current_match_mod = 0):
        self.name = name
        self.scores = scores
        self.auton_rate = auton_rate
        self.repair_time = repair_time
        self.robot_health = robot_health
        self.last_match_time = last_match_time
        self.current_match_mod = current_match_mod
        self.match_status = 1.0

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
        return cls(json_obj['name'], json_obj['scores'], json_obj['auton_rate'], json_obj['repair_time'], json_obj['robot_health'], json_obj['last_match_time'])

    def exportJSON(self):
        with open('team_data/' + self.name + '.json', 'w') as f:
            json.dump(self.__dict__, f)

    def give_score(self):
        self.last_match_time = str(datetime.now())
        raw_score = random.choice(self.scores)
        self.scores.remove(raw_score)
        score = int(round(raw_score * self.robot_health + self.current_match_mod))
        self.current_match_mod = 0
        self.exportJSON()
        return score
        
