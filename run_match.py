from team import Team
from colortext import *
import argparse
import os
import random
import shutil
import ansiwrap
from time import sleep


class MatchEvent():

    def __init__(self, time, team, color):
        self.time = time
        self.team = team
        self.color = color
        self.score_updates = [[0, 0, 0], [0, 0, 0], [0, 0, 0]] #[towers, red stacks, blue stacks]

    def teamcolored(self):
        if self.color == 1:
            return bluetext(self.team)
        else:
            return redtext(self.team)

    def log(self, text):
        log_string = ""
        if self.time < 15:
            log_string += "0:" + str(15 - self.time).zfill(2) + "\t"
        else:
            remaining = 120 - self.time
            log_string += str(remaining // 60) + ":" + str(remaining % 60).zfill(2) + "\t"
        log_string += text
        print(ansiwrap.fill(log_string, shutil.get_terminal_size().columns, subsequent_indent="\t"))

    def act(self):
        return self.score_updates #Should be overriden by all subclasses

class Stack(MatchEvent):

    def __init__(self, zone, time, team, color, cube_totals=None, cube_order=None, autofail=False):
        if (cube_totals == None) and (cube_order == None):
            raise ValueError("Bad stack created!")
        self.cube_totals = cube_totals
        self.cube_order = cube_order
        self.zone = zone
        if cube_order == None:
            self.cube_order = []
            for index in range(3):
                for i in range(cube_totals[index]):
                    self.cube_order.append(index)
            random.shuffle(self.cube_order)
        if cube_totals == None:
            self.update_totals()
        self.autofail = autofail
        super().__init__(time, team, color)

    def update_totals(self):
        new_totals = [0, 0, 0]
        for cube in self.cube_order:
            new_totals[cube] += 1
        self.cube_totals = new_totals

    def act(self):
        attempt_str = self.teamcolored() + " tries to stack " + cube_totals_to_string(self.cube_totals) + " in the "
        if self.zone == 0:
            attempt_str += "protected zone"
        else:
            attempt_str += "unprotected zone"
        self.log(attempt_str)
        if self.autofail:
            self.log("Stack misses!")
            self.cube_totals = [0, 0, 0]
        elif random.random() < 0.95:
            self.log("Success!")
        else:
            self.cube_order = self.cube_order[:random.randint(1, 3)]
            self.update_totals()
            self.log("STACK IS DROPPED! " + cube_totals_to_string(self.cube_totals) + " remain")
        self.score_updates[self.color + 1] = self.cube_totals
        return self.score_updates

class Destack(MatchEvent):

    def __init__(self, stack, time):
        self.stack = stack
        self.cube_totals = stack.cube_totals
        self.zone = stack.zone
        super().__init__(time, stack.team, stack.color)

    def act(self):
        self.cube_totals = self.stack.cube_totals
        event_str = self.teamcolored() + " removes " + cube_totals_to_string(self.cube_totals) + " from the "
        if self.zone == 0:
            event_str += "protected zone"
        else:
            event_str += "unprotected zone"
        self.log(event_str)
        self.score_updates[self.color + 1] = [total * -1 for total in self.cube_totals]
        return self.score_updates

class Tower(MatchEvent):

    tower_names = ["red alliance tower", "red half tower", "back field tower", "center tower", "front field tower", "blue half tower", "blue alliance tower"]

    def __init__(self, tower_loc, cube, time, team, color):
        self.tower_loc = tower_loc
        self.cube = cube
        super().__init__(time, team, color)

    def act(self):
        attempt_str = self.teamcolored() + " tries to tower "
        if self.cube == 0:
            attempt_str += orangetext("orange")
        elif self.cube == 1:
            attempt_str += greentext("green")
        elif self.cube == 2:
            attempt_str += purpletext("purple")
        attempt_str += " in the " + self.tower_names[self.tower_loc]
        self.log(attempt_str)
        if random.random() < 0.95:
            self.log("Success!")
            self.score_updates[0][self.cube] = 1
        else:
            self.log("Towering failed!")
        return self.score_updates


def cube_totals_to_string(totals):
    string = ""
    if totals[0] != 0:
        string += orangetext(str(totals[0]) + " orange cube")
        if (totals[0] > 1):
            string += orangetext("s")
    if totals[1] != 0:
        if len(string) != 0:
            if totals[2] == 0:
                string += " and "
            else:
                string += ", "
        string += greentext(str(totals[1]) + " green cube")
        if (totals[1] > 1):
            string += greentext("s")
    if totals[2] != 0:
        if len(string) != 0:
            string += " and "
        string += purpletext(str(totals[2]) + " purple cube")
        if (totals[2] > 1):
            string += purpletext("s")
    return string

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
    stacks[focus_cube] = random.randint(int(max_of_focus / 2), int(max_of_focus * 3 / 4))
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

def update_cubes(curr, delta):
    for i in range(3):
        for j in range(3):
            curr[i][j] += delta[i][j]

def pick_acting_team(strengths):
    random_result = random.uniform(0, sum(strengths))
    if random_result <= strengths[0]:
        strengths[0] /= 2
        return 0
    else:
        strengths[1] /= 2
        return 1

def get_all_more(more, less):
    for i in range(len(more)):
        if more[i] < less[i]:
            return False
    return True

def run_match(red_alliance, blue_alliance):
    red_strengths = [team.give_score() for team in red_alliance]

    blue_strengths = [team.give_score() for team in blue_alliance]

    red_score_gen = int(sum(red_strengths) / 2)
    blue_score_gen = int(sum(blue_strengths) / 2)

    #0 = orange, 1 = green, 2 = purple
    red_focus_cube = random.randint(0, 2)
    blue_focus_cube = random.randint(0, 2)

    towers_pred = [0, 0, 0]
    red_stacks_pred = [-1, 0, 0]
    blue_stacks_pred = [-1, 0, 0]

    attempts = 0

    while not get_valid_match(towers_pred, red_stacks_pred, blue_stacks_pred):
        if attempts == 10: #Score may be impossible?
            blue_score_gen -= 1
        if attempts == 20:
            red_score_gen -= 1
            attempts = 0
        towers_pred = gen_towers(red_focus_cube, blue_focus_cube)
        red_stacks_pred = gen_stacks(towers_pred, red_focus_cube, red_score_gen)
        blue_stacks_pred = gen_stacks(towers_pred, blue_focus_cube, blue_score_gen)

    #Calculate auton bonus
    red_auton_odds = red_alliance[0].auton_rate + red_alliance[1].auton_rate
    blue_auton_odds = blue_alliance[0].auton_rate + blue_alliance[1].auton_rate
    tie_auton_odds = 0.6 - abs(red_auton_odds - blue_auton_odds) / 2
    #print(red_auton_odds + blue_auton_odds + tie_auton_odds)
    auton_result_num = random.uniform(0, red_auton_odds + blue_auton_odds + tie_auton_odds)
    #print(auton_result_num)
    auton_winner = -1
    if auton_result_num < red_auton_odds:
        auton_winner = 0
    elif auton_result_num < red_auton_odds + blue_auton_odds:
        auton_winner = 1
    else:
        auton_winner = 2

    events = []
    match_totals = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    red_auton_result = [0, 0, 0]
    blue_auton_result = [0, 0, 0]

    red_p_auton = None
    red_u_auton = None
    blue_p_auton = None
    blue_u_auton = None

    #Auton generation
    p_autons = [[0, 0, 0], [0], [0, 2, 0, 0]] #Autons common for protected zone (red)
    u_autons = [[0, 2, 1, 2, 1, 1, 0], [0, 2, 1, 1, 0], [0, 2, 1, 1, 0, 2], [0, 2, 1, 1, 0, 0], [0]] #Autons common for unprotected zone (red)

    successful_auton_gen = False
    
    while not successful_auton_gen:

        red_auton_result = [0, 0, 0]
        blue_auton_result = [0, 0, 0]

        red_p = list.copy(random.choice(p_autons))
        red_u = list.copy(random.choice(u_autons))
        blue_p = list.copy(random.choice(p_autons))
        blue_u = list.copy(random.choice(u_autons))

        for i in range(len(blue_p)):
            if blue_p[i] == 0:
                blue_p[i] = 1
            elif blue_p[i] == 1:
                blue_p[i] = 0
        for i in range(len(blue_u)):
            if blue_u[i] == 0:
                blue_u[i] = 1
            elif blue_u[i] == 1:
                blue_u[i] = 0

        fails = [False, False, False, False]

        for i in range(4):
            if random.random() > 0.8:
                fails[i] = True

        red_autons = [red_p, red_u]
        blue_autons = [blue_p, blue_u]

        for i in range(2):
            if not fails[i]:
                for cube in red_autons[i]:
                    red_auton_result[cube] += 1
            if not fails[i + 2]:
                for cube in blue_autons[i]:
                    blue_auton_result[cube] += 1

        red_total = sum(red_auton_result)
        blue_total = sum(blue_auton_result)

        if (red_total > blue_total and auton_winner == 0) or (red_total < blue_total and auton_winner == 1) or (red_total == blue_total and auton_winner == 2): #We randomly picked right
            
            red_p_auton = Stack(0, random.randint(10, 14), red_alliance[0].name, 0, cube_order=red_p, autofail=fails[0])
            red_u_auton = Stack(1, random.randint(10, 14), red_alliance[1].name, 0, cube_order=red_u, autofail=fails[1])
            blue_p_auton = Stack(0, random.randint(10, 14), blue_alliance[0].name, 1, cube_order=blue_p, autofail=fails[2])
            blue_u_auton = Stack(1, random.randint(10, 14), blue_alliance[1].name, 1, cube_order=blue_u, autofail=fails[3])

            events = [red_p_auton, red_u_auton, blue_p_auton, blue_u_auton]

            successful_auton_gen = True
            
    #Stack event generation

    #Remove auton stacks as necessary (or cuz we feel like it)
    red_available_spots = 1
    blue_available_spots = 1
    destacks = []

    red_protected_spots = 1
    blue_protected_spots = 1
    red_unprotected_spots = 0
    blue_unprotected_spots = 0

    red_still_needed = [red_stacks_pred[i] - red_auton_result[i] for i in range(3)]
    blue_still_needed = [blue_stacks_pred[i] - blue_auton_result[i] for i in range(3)]

    stack_size_reasonable = False

    while not stack_size_reasonable:
        for event in events:
            if type(event) == Stack and event.autofail:
                if event.color == 0:
                    red_available_spots += 1
                    if event.zone == 0:
                        red_protected_spots += 1
                    else:
                        red_unprotected_spots += 1
                else:
                    blue_available_spots += 1
                    if event.zone == 0:
                        blue_protected_spots += 1
                    else:
                        blue_unprotected_spots += 1
            else:
                if event.color == 0 and (not get_all_more(red_stacks_pred, red_auton_result) or random.random() < 0.5):
                    destacks.append(Destack(event, random.randint(16, 25)))
                    red_available_spots += 1
                    for i in range(3):
                        red_auton_result[i] -= event.cube_totals[i]
                    if event.zone == 0:
                        red_protected_spots += 1
                    else:
                        red_unprotected_spots += 1
                elif event.color == 1 and (not get_all_more(blue_stacks_pred, blue_auton_result) or random.random() < 0.5):
                    destacks.append(Destack(event, random.randint(16, 25)))
                    blue_available_spots += 1
                    for i in range(3):
                        blue_auton_result[i] -= event.cube_totals[i]
                    if event.zone == 0:
                        blue_protected_spots += 1
                    else:
                        blue_unprotected_spots += 1
        if sum(red_still_needed) <= red_available_spots * 12 and sum(blue_still_needed) <= blue_available_spots * 12:
            stack_size_reasonable = True
    
    for event in destacks:
        events.append(event)

    red_still_needed = [red_stacks_pred[i] - red_auton_result[i] for i in range(3)]
    blue_still_needed = [blue_stacks_pred[i] - blue_auton_result[i] for i in range(3)]

    #Generate stacks to add
    try:
        red_stacks = [[0, 0, 0] for i in range(random.randint(int(sum(red_still_needed) / 12) + 1, red_available_spots))]
    except ValueError:
        red_stacks = [[0, 0, 0] for i in range(red_available_spots)]

    try:
        blue_stacks = [[0, 0, 0] for i in range(random.randint(int(sum(blue_still_needed) / 12) + 1, blue_available_spots))]
    except ValueError:
        blue_stacks = [[0, 0, 0] for i in range(blue_available_spots)]

    for i in range(3):
        for j in range(red_still_needed[i]):
            red_stacks[random.randint(0, len(red_stacks) - 1)][i] += 1
        for j in range(blue_still_needed[i]):
            blue_stacks[random.randint(0, len(blue_stacks) - 1)][i] += 1

    red_avail_zones = [0 for i in range(red_protected_spots)]
    if red_unprotected_spots == 1:
        red_avail_zones.append(1)
    blue_avail_zones = [0 for i in range(blue_protected_spots)]
    if blue_unprotected_spots == 1:
        blue_avail_zones.append(1)

    for stack in red_stacks:
        events.append(Stack(red_avail_zones.pop(random.randint(0, len(red_avail_zones) - 1)), random.randint(30, 120), red_alliance[pick_acting_team(red_strengths)].name, 0, cube_totals=stack))
    for stack in blue_stacks:
        events.append(Stack(blue_avail_zones.pop(random.randint(0, len(blue_avail_zones) - 1)), random.randint(30, 120), blue_alliance[pick_acting_team(blue_strengths)].name, 1, cube_totals=stack))

    #Generate tower event times
    tower_times = []
    for i in range(sum(towers_pred)):
        tower_times.append(random.randint(45, 120))
    tower_times.sort()

    #Quietly sim to determine what alliance should put each tower

    red_sim_results = [0, 0, 0]
    blue_sim_results = [0, 0, 0]
    events.sort(key=lambda x: x.time)
    tower_events = []
    curr_event = 0
    free_towers = [0, 1, 2, 3, 4, 5, 6]
    tower_colors_needed = []
    for i in range(3):
        for j in range(towers_pred[i]):
            tower_colors_needed.append(i)


    for time in range(0, 120):
        if curr_event < len(events) and events[curr_event].time == time:
            while curr_event < len(events) and events[curr_event].time == time:
                event = events[curr_event]
                if type(event) == Stack:
                    if event.color == 0:
                        for i in range(3):
                            red_sim_results[i] += event.cube_totals[i]
                    else:
                        for i in range(3):
                            blue_sim_results[i] += event.cube_totals[i]
                elif type(event) == Destack:
                    if event.color == 0:
                        for i in range(3):
                            red_sim_results[i] -= event.cube_totals[i]
                    else:
                        for i in range(3):
                            blue_sim_results[i] -= event.cube_totals[i]
                curr_event += 1
        if len(tower_times) == 0:
            break
        if tower_times[0] == time:
            tower_color = tower_colors_needed.pop(random.randint(0, len(tower_colors_needed) - 1))
            if red_sim_results[tower_color] > blue_sim_results[tower_color]:
                tower_team = 0
            elif red_sim_results[tower_color] < blue_sim_results[tower_color]:
                tower_team = 1
            else:
                tower_team = random.randint(0, 1)
            valid_tower = False
            tower_loc = 7
            while not valid_tower:
                tower_loc = random.choice(free_towers)
                if not ((tower_team == 0 and tower_loc == 6) or (tower_team == 1 and tower_loc == 0)):
                    valid_tower = True
                    free_towers.remove(tower_loc)
            if tower_team == 0:
                tower_events.append(Tower(tower_loc, tower_color, time, red_alliance[pick_acting_team(red_strengths)].name, 0))
            else:
                tower_events.append(Tower(tower_loc, tower_color, time, blue_alliance[pick_acting_team(blue_strengths)].name, 1))
            del tower_times[0]
    
    for event in tower_events:
        events.append(event)
            
    events.sort(key=lambda x: x.time)
    #Run match and log events
    curr_event = 0
    auton_winner = -1
    input("Press enter to begin")
    for time in range(121):
        sleep(0.5)
        if curr_event < len(events) and events[curr_event].time == time:
            while curr_event < len(events) and events[curr_event].time == time:
                update_cubes(match_totals, events[curr_event].act())
                curr_event += 1
        if time == 14:
            if sum(match_totals[1]) > sum(match_totals[2]):
                auton_winner = 0
                print(redtext("Red wins autonomous!"))
            elif sum(match_totals[1]) < sum(match_totals[2]):
                auton_winner = 1
                print(bluetext("Blue wins autonomous!"))
            else:
                print("Autonomous tie!")
                auton_winner = 2
            input("Press enter to begin driver control")
    red_final_score = calc_score(match_totals[0], match_totals[1])
    blue_final_score = calc_score(match_totals[0], match_totals[2])
    if auton_winner == 0:
        red_final_score += 6
    elif auton_winner == 1:
        blue_final_score += 6
    else:
        red_final_score += 3
        blue_final_score += 3
    print("Time up!")
    print("Towers: " + cube_totals_to_string(match_totals[0]))
    print("Red stacks: " + cube_totals_to_string(match_totals[1]))
    print("Blue stacks: " + cube_totals_to_string(match_totals[2]))

    print("Final score: " + redtext(red_final_score) + '-' + bluetext(blue_final_score))

'''
    for event in events:
        update_cubes(match_totals, event.act())
        #print(match_totals)
'''

    

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
    reds = [red1, red2]
    blues = [blue1, blue2]
    run_match(reds, blues)