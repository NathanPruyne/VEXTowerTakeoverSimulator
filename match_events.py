import random
import ansiwrap
import shutil
from colortext import *
from utils import *

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