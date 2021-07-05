"""Squad setting for app."""
from numpy import ndarray
from warunits import Soldier, Vehicle
from scipy.stats import gmean
from warconstants import MIN_RECHARGE_TIME, MAX_HP, MIN_HP


class Squad:
    def __init__(self, s_counter, v_counter, s_in_vehicle, name):
        self.__soldiers = list()
        for _ in range(s_counter):
            self.__soldiers.append(Soldier(MAX_HP, MIN_RECHARGE_TIME))
        self.__vehicles = list()
        for _ in range(v_counter):
            self.__vehicles.append(Vehicle(MAX_HP, MIN_RECHARGE_TIME, s_in_vehicle))
        self.__soldiers_in_vehicle = s_in_vehicle
        self.name = name

    def get_success_probability(self) -> ndarray:
        """Get the total success probability"""
        return gmean([soldier.attack_probability() for soldier in self.__soldiers]
                     + [vehicle.calculated_damage() for vehicle in self.__vehicles])

    def attack_squad(self, damage: float, tick: int) -> None:
        """Init attack on this squad"""
        calc_dmg = damage / (len(self.__soldiers) + len(self.__vehicles))
        for soldier in self.__soldiers:
            soldier.attack_unit(calc_dmg, tick)
        for vehicle in self.__vehicles:
            vehicle.attack_vehicle(calc_dmg, tick)

    @property
    def squad_hp(self) -> float:
        """Get the total squad health points."""
        hp_sum = MIN_HP
        for soldier in self.__soldiers:
            hp_sum += soldier.health

        for vehicle in self.__vehicles:
            hp_sum += vehicle.health

        return hp_sum

    def calculated_damage(self) -> float:
        """Get the calculated damage for attack."""
        dmg_sum = MIN_HP
        for soldier in self.__soldiers:
            dmg_sum += soldier.calculated_damage()
        for vehicle in self.__vehicles:
            dmg_sum += vehicle.calculated_damage()
        return dmg_sum
