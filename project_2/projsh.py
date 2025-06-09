import random



class Human:
    def __init__(self, name):
        self.name = name

class FootballPlayer(Human):
    def __init__(self, name):
        super().__init__(name)
        self.team = None

    def assign_team(self, team_name):
        self.team = team_name

player_names = [
    'hossein', 'maziyar', 'akbar', 'nima', 'mehdi', 'farhad', 'mohammad', 'khashayar', 'milad', 'mostafa', 'amin',
    'saeed', 'pooya', 'pooria', 'reza', 'ali', 'behzad', 'soheil', 'behrooz', 'shahrooz', 'saman', 'mohsen'
]

players = [FootballPlayer(name) for name in player_names]

random.shuffle(players)

for i, player in enumerate(players):
    if i < 11:
        player.assign_team('A')
    else:
        player.assign_team('B')

for player in players:
    print(f' {player.name},{player.team}')
