import logging
import wararmy
from random import seed
import reader
import game


def main():
    json_reader = reader.JSONReader("config.json")
    fname = json_reader.check_for_copy()
    if fname != "":
        print(f"Results already calculated in {fname}")
        exit(0)
    else:
        json_reader.create_new_log()
        json_reader.initiate_logger()

    data = json_reader.get_parsed()
    seed(data['seed'])
    team_list = list()
    for i in data['teams']:
        team_list.append(wararmy.Army(i['strategy'],
                                      i["count of squads"],
                                      i["count of soldiers"],
                                      i["count of soldiers in vehicle"],
                                      i["count of vehicles"],
                                      i["name"], ))
    logging.info('Start GAME!')
    logging.info('------------------')

    play = game.Game()
    play.start_game(team_list)


if __name__ == '__main__':
    main()
