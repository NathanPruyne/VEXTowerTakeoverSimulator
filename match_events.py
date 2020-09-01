import random
import ansiwrap
import shutil
from colortext import *
from utils import *
from PyQt5 import QtCore, QtGui, QtWidgets
from visualization import Bot, Cube
import constants

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

    def visualize(self, window):
        pass #Should be overriden by all subclasses

    def init_visualization(self, window):
        pass #Should be overriden by subclasses

class Stack(MatchEvent):

    def __init__(self, location, time, team, color, cube_totals=None, cube_order=None, autofail=False):
        if (cube_totals == None) and (cube_order == None):
            raise ValueError("Bad stack created!")
        self.cube_totals = cube_totals
        self.cube_order = cube_order
        self.location = location
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
        if self.location == 0:
            attempt_str += "unprotected zone"
        else:
            attempt_str += "protected zone"
        self.log(attempt_str)
        if self.autofail:
            self.log("Stack misses!")
            self.cube_visuals = []
            self.cube_totals = [0, 0, 0]
        elif random.random() < constants.STACK_SUCCESS_ODDS:
            self.log("Success!")
        else:
            cubes_remaining = random.randint(1, 3)
            self.cube_order = self.cube_order[:cubes_remaining]
            self.cube_visuals = self.cube_visuals[:cubes_remaining + 1]
            self.update_totals()
            self.log("STACK IS DROPPED! " + cube_totals_to_string(self.cube_totals) + " remain")
        self.score_updates[self.color + 1] = self.cube_totals
        return self.score_updates

    def init_visualization(self, window):
        self.cube_visuals = []
        max_color = self.cube_totals.index(max(self.cube_totals))
        top_loc = Cube.stack_top_locs[self.color][self.location]
        top_cube = Cube(window, max_color, top_loc[0], top_loc[1], self.team + str(self.location) + str(self.time))
        top_cube.hide()
        self.cube_visuals.append(top_cube)
        stack_loc = Cube.full_stack_locs[self.color][self.location]
        count = 0
        for color in self.cube_order:
            cube_vis = Cube(window, color, stack_loc[0], stack_loc[1] - count * 51, self.team + str(self.location) + str(self.time))
            cube_vis.hide()
            self.cube_visuals.append(cube_vis)
            count += 1


    def visualize(self, window):
        acting_bot = window.findChild(QtWidgets.QLabel, self.team)
        loc = list(Bot.zone_locs_and_rots[self.color][self.location])
        if self.autofail:
            loc[0] += random.randint(-40, 40)
            loc[1] += random.randint(-40, 40)
            loc[2] += random.randint(-10, 10)
        acting_bot.update_position(loc[0], loc[1], loc[2])
        for cube in self.cube_visuals:
            cube.show()
        #print(window.findChildren(QtWidgets.QLabel))

class Destack(MatchEvent):

    def __init__(self, stack, time):
        self.stack = stack
        self.cube_totals = stack.cube_totals
        self.location = stack.location
        super().__init__(time, stack.team, stack.color)

    def act(self):
        self.cube_totals = self.stack.cube_totals
        event_str = self.teamcolored() + " removes " + cube_totals_to_string(self.cube_totals) + " from the "
        if self.location == 0:
            event_str += "unprotected zone"
        else:
            event_str += "protected zone"
        self.log(event_str)
        self.score_updates[self.color + 1] = [total * -1 for total in self.cube_totals]
        return self.score_updates
    
    def visualize(self, window):
        acting_bot = window.findChild(QtWidgets.QLabel, self.team)
        loc = Bot.zone_locs_and_rots[self.color][self.location]
        acting_bot.update_position(loc[0], loc[1], loc[2])
        for cube in self.stack.cube_visuals:
            cube.hide()

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
        if random.random() < constants.TOWER_SUCCESS_ODDS:
            self.log("Success!")
            self.score_updates[0][self.cube] = 1
        else:
            self.log("Towering failed!")
            self.cube_visual = None
        return self.score_updates

    def init_visualization(self, window):
        visual_loc = Cube.tower_locs[self.tower_loc]
        self.cube_visual = Cube(window, self.cube, visual_loc[0], visual_loc[1], self.team + str(self.tower_loc) + str(self.time))
        self.cube_visual.hide()

    def visualize(self, window):
        acting_bot = window.findChild(QtWidgets.QLabel, self.team)
        loc = Bot.tower_locs_and_rots[self.color][self.tower_loc]
        acting_bot.update_position(loc[0], loc[1], loc[2])
        if self.cube_visual:
            self.cube_visual.show()