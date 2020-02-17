import random

from kicker_arena import Player, Team, Match, Record, Season


random.seed(20200214)

player_names = ["A",
                "B",
                "C",
                "D",
                "E",
                "F",
                "G",
                "H",
                "I",
                "J"]

warmup_season = Season(player_names)
warmup_season.show_matches()

warmup_season.add_record(Record("tiger:bear", "8:10"))
warmup_season.add_record(Record("bear:snake", "7:10"))
warmup_season.add_record(Record("snake:dolphin", "10:8"))
# warmup_season.add_record(Record("dolphin:camel", "10:2"))
# warmup_season.add_record(Record("camel:tiger", "10:7"))

# warmup_season.show_pointsboard()

print("remaining matches: ")
warmup_season.show_remain_matches()
warmup_season.load_points_from_records()
print(warmup_season.pointsboard)

# professional_season = warmup_season.random_restart()
professional_season = warmup_season.switch_members()


print("professional season matches:")
professional_season.show_matches()

print(professional_season.pointsboard)
