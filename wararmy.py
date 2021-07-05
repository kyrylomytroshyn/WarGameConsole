"""Army setting for app."""
from numpy import ndarray

from warsquad import Squad
from scipy.stats import gmean
from random import randint
import warnings


class Army:
    def __init__(self,
                 strategy: str,
                 number_of_squads: int,
                 number_of_units: int,
                 number_of_units_in_car: int,
                 number_of_vehicle: int,
                 name):
        self.strategy = strategy
        self.squads = list()
        self.name = name
        for i in range(number_of_squads):
            self.squads.append(Squad(number_of_units, number_of_units_in_car, number_of_vehicle, name))
        warnings.filterwarnings("ignore", category=RuntimeWarning)

    def attack_army(self, damage: float, tick: int) -> None:
        """Init attack on army.

        Arguments:
            Damage -> damage from enemy.
            Tick -> Game tick.
        """
        for squad in self.squads:
            squad.attack_squad(damage/len(self.squads), tick)

    def get_army_attack_probability(self) -> ndarray:
        """Returns army total probability"""
        return gmean([squad.get_success_probability() for squad in self.squads])

    def get_army_dmg(self) -> ndarray:
        """Returns average of army total damage"""
        return gmean([squad.calculated_damage() for squad in self.squads])

    def choose_weakest_army(self, armies: list):
        """Choosing the weakest army from list."""
        weakest_iterator = 0
        unique_arr = set(armies)
        if len(unique_arr) == len(armies):
            return self.choose_random_army(armies)
        for iterator in range(len(armies) - 1):

            if armies[weakest_iterator].get_army_hp() > armies[iterator].get_army_hp() > 0 \
                    and armies[iterator] != self:
                weakest_iterator = iterator

        if armies[weakest_iterator] == self:
            return self.choose_random_army(armies)
        return armies[weakest_iterator]

    def choose_strongest_army(self, armies: list):
        """Choosing the strongest army from list."""
        strongest_iterator = 0

        unique_arr = set(armies)
        if len(unique_arr) == len(armies):
            return self.choose_random_army(armies)

        for iterator in range(len(armies)):
            if armies[strongest_iterator].get_army_hp() < armies[iterator].get_army_hp() > 0 \
                    and armies[iterator] != self:
                strongest_iterator = iterator

        if armies[strongest_iterator] == self:
            return self.choose_random_army(armies)
        return armies[strongest_iterator]

    def choose_random_army(self, armies: list):
        """Choosing the random army from list."""
        iterator = randint(0, len(armies)-1)
        while armies[iterator] != self:
            iterator = randint(0, len(armies) - 1)
        return armies[iterator]

    def get_army_hp(self) -> float:
        """Get total health points of army"""
        return sum([squad.squad_hp for squad in self.squads])
