import random
import pandas as pd
import matplotlib.pyplot as plt

from utils import TuplesGenerator


class Player:
    def __init__(self, name, points):
        self.name = name
        self.points = points


class Team:
    """
    Two Players

    """
    def __init__(self, name, players):
        self.name = name
        self.players = players

    def __str__(self):
        return "Team {name} \t({p1} and {p2})".format(name=self.name,
                                                      p1=self.players[0].name,
                                                      p2=self.players[1].name)

    def scoring_dict(self, points):
        return {self.players[0].name: points, self.players[1].name: points}


class Match:
    """
    Two Teams

    """
    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2

    def __str__(self):
        return "{} \t vs \t {}".format(self.team1, self.team2)

    @property
    def team_names(self):
        return [self.team1.name, self.team2.name]

    def demonstrate(self):
        print(str(self))


class Record:

    def __init__(self, team_names, scores):
        """

        :param: String, eg. "tiger:bat"
        :param: String, eg. "8:10"
        """

        self.team_names = team_names.split(":")
        self.scores = [int(score) for score in scores.split(":")]

    def pointsboard(self, teams):
        """
        Record object does not know the team it refers to.
        So it needs Team objects to calculate the points for each player.

        :param teams: list of Teams
        :return: dict, the pointsboard for the teams who joined the match of this record.
           pointsboard is like :
             {
                "player1": 10,
                "player2": 8,
                ...
             }
        """

        pointsboard = {}
        for i in range(len(self.team_names)):
            notify_teams = [team for team in teams if team.name == self.team_names[i]]
            for team in notify_teams:
                pointsboard.update(team.scoring_dict(self.scores[i]))
        return pointsboard


class Season:
    team_names = ["bat", "elephant", "bear", "dolphin", "camel", "tiger", "snake", "lion", "panda"]

    def __init__(self, names):
        self.players = [Player(name, 0) for name in names]
        self.teams = []
        self.records = []
        self.matches = []
        self.finished_matches = []

        self.generate_teams()  # warning! this will shuffle the players and resign team names
        self.generate_matches()

    @property
    def remain_matches(self):
        return [match for match in self.matches if str(match) not in [str(match) for match in self.finished_matches]]

    @property
    def pointsboard(self):
        pointsboard = {}
        for player in self.players:
            pointsboard.update({player.name: player.points})
        return pointsboard

    def generate_teams(self):
        random.shuffle(self.team_names)
        random.shuffle(self.players)

        teams = []
        for i, (p1, p2) in enumerate(TuplesGenerator.generate_tuples_lr_shuffle(self.players)):
            teams.append(Team(self.team_names[i], [p1, p2]))
        self.teams = teams

    def generate_matches(self, gap=1, match_type="wheel"):
        if match_type == "wheel":
            self.matches = [Match(*team_tuple) for team_tuple in TuplesGenerator.generate_wheels(self.teams, gap)]
        else:
            self.matches = [Match(*team_tuple) for team_tuple in TuplesGenerator.generate_tuples(self.teams)]

    # functions
    def add_record(self, record):
        """

        :param: record: Record
        """
        for match in self.matches:
            if set(match.team_names) == set(record.team_names):
                self.finished_matches.append(match)
                self.records.append(record)
                break

    def load_points_from_records(self):
        for record in self.records:
            self.load_points_from_pointsboard(record.pointsboard(self.teams))

    def load_points_from_pointsboard(self, pointsboard):
        """

        pointsboard: dict: {player_name: points}
        """

        for player in self.players:
            if player.name in pointsboard:
                player.points += pointsboard[player.name]

    # next season
    def switch_members(self, n_member_switch=1, n_match_switch=2, keep_points=True):
        """

        :param n_member_switch: int, number of switches for players in teams
        :param n_match_switch: int, number of switches for teams in matches
        :param keep_points: bool, keep the tracking of points of players or not
        :return: a Season object
        """

        # decide which player stay in the team
        fix_index = [random.randint(0, 1) for _ in range(len(self.teams))]

        fixed_players  = [team.players[1 - fix_index[i]]     for i, team in enumerate(self.teams)]
        switch_players = [team.players[fix_index[i]] for i, team in enumerate(self.teams)]

        # do the player switch operation
        switched_players = [switch_players[n - n_member_switch] for n in range(len(switch_players))]

        teams = []
        for i, (p1, p2) in enumerate(zip(fixed_players, switched_players)):
            teams.append(Team(self.team_names[i], [p1, p2]))

        season = Season([p.name for p in self.players])  # p.s. only names are kept, points are lost
        season.teams = teams
        season.generate_matches(gap=n_match_switch)

        if keep_points:
            season.load_points_from_pointsboard(self.pointsboard)

        return season

    def random_restart(self, keep_points=True):
        """

        :param keep_points: bool, keep the tracking of points of players or not
        :return: a Season object.
        """

        season = Season([p.name for p in self.players]) # p.s. only names are kept, points are lost

        if keep_points:
            season.load_points_from_pointsboard(self.pointsboard)

        return season

    # displays
    def show_matches(self):
        for match in self.matches:
            match.demonstrate()

    def show_remain_matches(self):
        for match in self.remain_matches:
            match.demonstrate()

    def show_pointsboard(self):

        self.load_points_from_records()

        pb = self.pointsboard
        df = pd.DataFrame({
            "player":    list(pb.keys()),
            "KC-points": list(pb.values())
        })
        df = df.sort_values(by=["KC-points"])
        df.plot.barh(x="player", y="KC-points")
        plt.show()
