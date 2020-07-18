from team import Team
import os

def gen_object(scoreset_file):
    team = Team.fromScoresetFile(scoreset_file)
    team.exportJSON()

if __name__ == "__main__":
    for file in os.listdir('scoresets'):
        full_path = 'scoresets/' + file
        if os.path.isfile(full_path) and full_path.split('.')[-1] == 'txt':
            gen_object(full_path)