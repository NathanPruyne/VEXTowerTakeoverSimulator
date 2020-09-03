from generatescoreset import get_score_set

if __name__ == "__main__":
    with open('teamlist.txt', 'r') as fp:
        for team in fp.readlines():
            name = team.strip()
            print(name)
            get_score_set(name)