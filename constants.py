import random

ORANGE_CUBE = 0
GREEN_CUBE = 1
PURPLE_CUBE = 2

UNPROTECTED_ZONE = 0
INNER_PROTECTED_ZONE = 1
OUTER_PROTECTED_ZONE = 2

STACK_SUCCESS_ODDS = 0.95
TOWER_SUCCESS_ODDS = 0.95

DEFAULT_SPEED = 0.5

PREMATCH_ODDS_GRID = {
    'IncreaseOneScore': 40,
    'DecreaseOneScore': 20,
    'IncreaseAllScores': 30,
    'DecreaseAllScores': 15,
    'ImproveAuton': 30,
    'WorsenAuton': 10
}

def give_prematch_event():
    picker = []

    for event_type in PREMATCH_ODDS_GRID:
        for i in range(PREMATCH_ODDS_GRID[event_type]):
            picker.append(event_type)
    
    return random.choice(picker)

DEFENSE_ODDS = 0.1
DEFENSE_CONTINUE_ODDS = 0.5
DEFENSE_TIMEOUT = 15