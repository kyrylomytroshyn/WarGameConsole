"""Units settings for app."""

from warconstants import (
    MAX_HP,
    MIN_HP,
    MIN_EXP,
    MAX_EXP,
    VEHICLE_DAMAGE_PERCENT,
    VEHICLE_DRIVER_DAMAGE_PERCENT,
    VEHICLE_OPERATORS_DAMAGE_PERCENT
)
import random
from scipy.stats import gmean


class Unit:

    def __init__(self, health: float, recharge: int):
        if MIN_HP > health or MAX_HP < health:
            raise ValueError(f"Count oh Health points can't be negative or higher than {MAX_HP}")
        self._health = health
        self._is_active = True
        self._recharge = 100

    @property
    def health(self) -> float:
        """Returns health points of Unit"""
        return self._health

    @property
    def recharge(self) -> int:
        """Returns recharge time in milliseconds of Unit"""
        return self._recharge

    @health.setter
    def health(self, hp: float) -> None:
        """Sets health points.

        Arguments:
             hp -- count of Health Points to set (0-100)
        """
        if not isinstance(hp, (int, float)):
            raise TypeError("Count of HP can be only numeric (float/int).")
        if MIN_HP >= hp >= MAX_HP:
            raise ValueError(f"Count oh Health points can't be negative or higher than {MAX_HP}")
        if hp <= MIN_HP:
            self._is_active = False
        self._health = hp

    @recharge.setter
    def recharge(self, time) -> None:
        """Sets recharge time in ms.

        Args:
             time -- recharge time in ms (100-2000)
        """
        self._recharge += time

    @property
    def is_active(self) -> bool:
        """Returns status of Unit (Alive = True, Dead = False)"""
        return self._is_active

    @is_active.setter
    def is_active(self, status: bool) -> None:
        """Returns status of Unit (Alive = True, Dead = False)"""
        self._is_active = status


class Soldier(Unit):
    """Soldier settings for game."""

    def __init__(self, health: float, recharge: int):
        super().__init__(health, recharge)
        self.__experience = 0
        self._personal_tick = 0
        self.recharge = 1000

    @property
    def experience(self) -> int:
        """Returns count of unit EXP"""
        return self.__experience

    @experience.setter
    def experience(self, value) -> None:
        """Sets count of Unit Experience.

        :arg value -- count of settable EXP (0-50)

        """
        if not isinstance(value, int):
            raise TypeError("Experience can be presented only by integer.")
        if MIN_EXP >= value >= MAX_EXP:
            raise ValueError(f"Experience can be set between {MIN_EXP} and {MAX_EXP}")
        self.__experience = value

    def attack_unit(self, damage, tick) -> bool:
        """Gives a damage to Unit

        :arg damage -- count of damage, gived to unit.

        :returns True if Unit alive, False if Unit destroyed.

        """
        if tick >= self._personal_tick:
            self.health -= damage
            if self.health <= 0:
                self._is_active = False

            self._personal_tick += self.recharge
            return True
        return False

    def calculated_damage(self):
        """Return a calculated damage by experience of soldier"""
        if not self._is_active:
            return 0
        dmg = 0.05 + self.__experience / 100
        self.lvl_up()
        return dmg

    def attack_probability(self):
        """Return probability of success attack. """
        if not self._is_active:
            return 0
        temp_prb = random.uniform(50 + self.__experience, 100)
        return 0.5 * (1 + self.health / 100) * temp_prb / 100

    def lvl_up(self):
        if self.__experience < MAX_EXP:
            self.__experience += 1


class Vehicle(Unit):
    """Vehicle settings for game."""

    def __init__(self, health: float, recharge: int, count_of_soldiers: int):
        super().__init__(health, recharge)
        self.__soldiers = [Soldier(100, 100) for _ in range(count_of_soldiers)]
        self._recharge = 2000
        self._personal_tick = 0

    def attack_probability(self) -> float:
        """Return probability of success attack. """
        if not self._is_active:
            return 0
        return 0.5 * (1 + self.health / 100) * gmean(
            [soldier.attack_probability() for soldier in self.soldiers]
        )

    @property
    def soldiers(self) -> list:
        return self.__soldiers

    def calculated_damage(self) -> float:
        """Return a calculated damage by experience of Vehicle"""
        if not self._is_active:
            return 0
        return 0.1 + sum([soldier.calculated_damage() for soldier in self.soldiers])

    def attack_vehicle(self, damage, tick) -> bool:
        """Gives a damage to Vehicle

        Arguments:
             damage -- count of damage, gived to unit.

        Returns:
             True if Unit alive, False if Unit destroyed.
        """
        if tick >= self._personal_tick:
            self.health -= damage * VEHICLE_DAMAGE_PERCENT
            if self.health <= 0:
                self._is_active = False
            # Getting the index of the vehicle driver.
            soldier_driver_number = random.randint(0, len(self.__soldiers) - 1)
            self.__soldiers[soldier_driver_number].attack_unit(damage * VEHICLE_DRIVER_DAMAGE_PERCENT, tick)
            # Giving damage to other.
            for i in range(len(self.__soldiers)):
                if i != soldier_driver_number:
                    self.__soldiers[i].attack_unit(damage * VEHICLE_OPERATORS_DAMAGE_PERCENT, tick)
            self._personal_tick += self.recharge
            return True
        return False

    def get_amount_hp(self):
        """Gives the amount HP of Vehicle Team (Mean of Vehicle and Soldiers)"""
        return (self.health + sum([soldier.health for soldier in self.__soldiers])) / (len(self.soldiers) + 1)
