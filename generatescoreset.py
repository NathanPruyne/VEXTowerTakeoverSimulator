import requests
import argparse

def get_score_set(team):
    
    match_request_args = {'team': team, 'season': 'Tower Takeover'}
    match_request = requests.get('https://api.vexdb.io/v1/get_matches', params=match_request_args)
    matches_json = match_request.json()

    top_scores = []

    for match in matches_json['result']:
        if match['red1'] == team or match['red2'] == team:
            match_score = match['redscore']
        elif match['blue1'] == team or match['blue2'] == team:
            match_score = match['bluescore']
        else:
            match_score = 0
        if len(top_scores) < 15:
            top_scores.append(match_score)
        elif top_scores[0] < match_score:
            top_scores[0] = match_score
        #print("Match score: " + str(match_score))
        #print("Current top scores: " + str(top_scores))
        top_scores.sort()

    if len(top_scores) < 15:
        while (2 * len(top_scores) - 15 < 0):
            top_scores.extend(top_scores)
        top_scores.extend(top_scores[2 * len(top_scores) - 15:])
        


    match_request_args = {'team': team, 'season': 'Tower Takeover', 'round': 2}
    match_request = requests.get('https://api.vexdb.io/v1/get_matches', params=match_request_args)
    qual_matches_json = match_request.json()
    num_matches = len(qual_matches_json['result'])

    rankings_request_args = {'team': team, 'season': 'Tower Takeover'}
    rankings_request = requests.get('https://api.vexdb.io/v1/get_rankings', params=rankings_request_args)
    rankings_json = rankings_request.json()

    total_ap = 0

    for event in rankings_json['result']:
        total_ap += event['ap']

    auton_win_rate = total_ap / 6.0 / num_matches

    f = open("team_data/" + team + ".txt", 'w')
    f.write(','.join([str(s) for s in top_scores]) + '\n' + str(auton_win_rate) + '\n')
    print(','.join([str(s) for s in top_scores]) + '\n' + str(auton_win_rate))
    f.close()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compile top 15 results for a team to generate score set and auton win rate for simulation')
    parser.add_argument('team', help='Team number of the team to get scores for')
    args = parser.parse_args()
    get_score_set(args.team)