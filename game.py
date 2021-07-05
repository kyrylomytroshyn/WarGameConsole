import logging


class Game:
    def __init__(self):
        pass

    def start_game(self, team_list: list):
        tick = 0
        while 1:
            tick += 500.0
            for team in team_list:
                if team.strategy == "Weakest":
                    enemy_team = team.choose_weakest_army(team_list)
                elif team.strategy == "Strongest":
                    enemy_team = team.choose_strongest_army(team_list)
                else:
                    enemy_team = team.choose_random_army(team_list)

                if enemy_team.get_army_hp() > 0:
                    if team.get_army_attack_probability() >= enemy_team.get_army_attack_probability():
                        damage = team.get_army_dmg()
                        enemy_team.attack_army(damage, tick)
                        logging.info(f"Attacked {enemy_team.name} with {damage} damage.")
                        logging.info(f"{enemy_team.name} -> {enemy_team.get_army_hp()} hp.")
                    else:
                        continue
                else:
                    print(f"{enemy_team.name} defeated.")
                    logging.info(f"{enemy_team.name} defeated.")
                    team_list.remove(enemy_team)
                    if len(team_list) == 1:
                        print(f"GAME OVER! Look into logs/wargame.log. WINNER IS {team_list[0].name}")
                        logging.info(f"GAME OVER! Look into logs/wargame.log. WINNER IS {team_list[0].name}")
                        exit(0)
