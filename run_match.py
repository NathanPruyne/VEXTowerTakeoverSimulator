from team import Team
import argparse
import os
import random

def run_match(red1, red2, blue1, blue2):
    red_score = int((red1.give_score() + red2.give_score()) / 2)
    blue_score = int((blue1.give_score() + blue2.give_score()) / 2)
    red_auton_odds = red1.auton_rate + red2.auton_rate
    blue_auton_odds = blue1.auton_rate + blue2.auton_rate
    tie_auton_odds = 0.6 - abs(red_auton_odds - blue_auton_odds) / 2
    print(red_auton_odds + blue_auton_odds + tie_auton_odds)
    auton_result_num = random.uniform(0, red_auton_odds + blue_auton_odds + tie_auton_odds)
    print(auton_result_num)
    if auton_result_num < red_auton_odds:
        print("Red wins auton!")
        red_score += 6
    elif auton_result_num < red_auton_odds + blue_auton_odds:
        print("Blue wins auton!")
        blue_score += 6
    else:
        print("Auton tie!")
        red_score += 3
        blue_score += 3
    print("Final score: " + str(red_score) + "-" + str(blue_score))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Simulate a competition match')
    parser.add_argument('red1', help='Red alliance team 1')
    parser.add_argument('red2', help='Red alliance team 2')
    parser.add_argument('blue1', help='Blue alliance team 1')
    parser.add_argument('blue2', help='Blue alliance team 2')
    args = parser.parse_args()
    try:
        red1 = Team.fromJSON('team_data/' + args.red1 + '.json')
        red2 = Team.fromJSON('team_data/' + args.red2 + '.json')
        blue1 = Team.fromJSON('team_data/' + args.blue1 + '.json')
        blue2 = Team.fromJSON('team_data/' + args.blue2 + '.json')
    except FileNotFoundError as err:
        print("Team file not found for team " + os.path.splitext(os.path.basename(err.filename))[0])
        quit()
    run_match(red1, red2, blue1, blue2)