from team import Team
from colortext import *
import argparse
import os
import random

def calc_score(towers, stacks):
    score = 0
    for i in range(3):
        score += stacks[i] * (towers[i] + 1)
    return score

def get_valid_match(towers, red_stacks, blue_stacks): #Checks if match score is valid
    if red_stacks[0] == -1 or blue_stacks[0] == -1: #Score generation failed
        return False
    for i in range(3):
        if towers[i] + red_stacks[i] + blue_stacks[i] > 22:
            return False
    return True

def gen_towers(focus1, focus2):
    towers = [random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)]

    if focus1 == focus2:
        towers[focus1] = random.randint(2, 4)
    else:
        towers[focus1] = random.randint(1, 3)
        towers[focus2] = random.randint(1, 3)
    
    if sum(towers) > 7:
        return gen_towers(focus1, focus2)
    else:
        return towers

def gen_stacks(towers, focus_cube, score):
    stacks = [0, 0, 0]
    max_of_focus = int(score / (towers[focus_cube] + 1))
    #print("Max of focus: " + str(max_of_focus))
    stacks[focus_cube] = random.randint(int(max_of_focus / 2), int(max_of_focus * 3 /4))
    not_focus = [i for i in range(3) if i != focus_cube]
    attempts = 0
    while calc_score(towers, stacks) != score:
        index = random.randint(0,1)
        add_cube = not_focus[index]
        stacks[add_cube] += 1
        if calc_score(towers, stacks) > score:
            stacks[add_cube] -= 1
            if index == 0:
                stacks[1] += 1
            else:
                stacks[0] += 1
            if calc_score(towers, stacks) > score:
                attempts += 1
                for i in not_focus:
                    stacks[i] == 0
                stacks[focus_cube] = random.randint(int(max_of_focus / 2), max_of_focus)
        if attempts > 10:
            stacks[0] = -1 #Stack generation failed
            return stacks
    return stacks


def run_match(red1, red2, blue1, blue2):
    red_score = int((red1.give_score() + red2.give_score()) / 2)
    blue_score = int((blue1.give_score() + blue2.give_score()) / 2)

    #0 = orange, 1 = green, 2 = purple
    red_focus_cube = random.randint(0, 2)
    blue_focus_cube = random.randint(0, 2)

    towers = [0, 0, 0]
    red_stacks = [-1, 0, 0]
    blue_stacks = [-1, 0, 0]

    attempts = 0

    while not get_valid_match(towers, red_stacks, blue_stacks):
        if attempts == 10: #Score may be impossible?
            blue_score -= 1
        if attempts == 20:
            red_score -= 1
            attempts = 0
        towers = gen_towers(red_focus_cube, blue_focus_cube)
        red_stacks = gen_stacks(towers, red_focus_cube, red_score)
        blue_stacks = gen_stacks(towers, blue_focus_cube, blue_score)

    print(red_score)
    print(blue_score)
    print(towers)
    print(red_stacks)
    print(blue_stacks)

    #Calculate auton bonus
    red_auton_odds = red1.auton_rate + red2.auton_rate
    blue_auton_odds = blue1.auton_rate + blue2.auton_rate
    tie_auton_odds = 0.6 - abs(red_auton_odds - blue_auton_odds) / 2
    #print(red_auton_odds + blue_auton_odds + tie_auton_odds)
    auton_result_num = random.uniform(0, red_auton_odds + blue_auton_odds + tie_auton_odds)
    #print(auton_result_num)
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