"""
    This file is part of callofcthulhu.

    callofcthulhu is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from typing import Optional

from coc.core.gender import Gender
from coc.core.roll import Roll, random_func, D100, D10
from coc.lib.logger import LOGGER


class Attribute:
    """
    Keep track of value, half and fifth
    """

    def __init__(self, description: str, code: str, regular: int = None, maximum: int = 100):
        LOGGER.debug(f"creating Attribute wir description:{description} code:{code} regular:{regular} maximum:{maximum}")
        self.description = description
        self.code = code
        self.maximum = maximum
        self._regular = regular
        self._half = regular // 2
        self._fifth = regular // 5
        LOGGER.info(f"Created {self.__repr__()}")

    def __repr__(self):
        return f'{self.description}{"" if self.code is None else f"/{self.code}"}({"Not yet set" if self.regular is None else f"R: {self._regular} H:{self._half} F: {self._fifth}"})'

    @property
    def regular(self) -> int:
        """
        Get regular value
        :return: regular value
        """
        return self._regular

    @regular.setter
    def regular(self, new_value: int) -> None:
        """
        Setter for regular
        :param new_value: new value (limited to the maximum)
        """
        LOGGER.debug(f"Trying to set {self} to {new_value}")
        if new_value > self.maximum:
            LOGGER.debug(f"{new_value} exceeds maximum of {self.maximum}, so limiting it so maximum")
            new_value = self.maximum
        self._regular = new_value
        self._half = new_value // 2
        self._fifth = new_value // 5

    @staticmethod
    def _compare(value: int, limit: Optional[int]) -> bool:
        """
        Verify if a value is lower than a limit. If no value is provided a random(100) will be generated
        :param value:  Value or None. In case of None a random value wil lbe generated.
        :param limit: Upper limit
        :return: True if value is less than or equal to limit.
        """
        if value is None:
            value = random_func(100)
        return value <= limit

    def is_regular(self, value: Optional[int]) -> bool:
        """
        Perform a regular check
        :param value: Value to check, if no value is provided a random(100) will be generated
        :return: True if value is less than or equal to _regular
        """
        return self._compare(value, self._regular)

    def is_hard(self, value: Optional[int]) -> bool:
        """
        Perform a hard check
        :param value: Value to check, if no value is provided a random(100) will be generated
        :return: True if value is less than or equal to _half
        """
        return self._compare(value, self._half)

    def is_extreme(self, value: Optional[int]) -> bool:
        """
        Perform an extreme hard check
        :param value: Value to check, if no value is provided a random(100) will be generated
        :return: True if value is less than or equal to _fifth
        """
        return self._compare(value, self._fifth)

    def deduct(self, value: int) -> None:
        """
        Subtract a value from this attribute
        :param value: value to subtract
        """
        LOGGER.info(f"Deducting {value} from {self}")
        self.regular -= value

    def set_if_higher(self, value) -> None:
        """
        Set the attribute value to a new value, but only ifg the new value is higher
        :param value: possible new value
        """
        if value > self.regular:
            self.regular = value

    def improvement_roll(self, count: int = 1) -> None:
        """
        Perform one or more improvements roll on this attribute
        :param count: Number of improvements rolls to perform
        """
        for _ in range(count):
            v = D100.roll()
            if v > self.regular:
                v = D10.roll()
                self.regular += v


STR = "STR"
CON = "CON"
DEX = "DEX"
SIZ = "SIZ"
APP = "APP"
INT = "INT"
POW = "POW"
EDU = "EDU"
LUCK = "LUCK"


class Characteristic(Attribute):
    """
    Investigator characteristic
    """

    def __init__(self, code, description, regular, maximum):
        Attribute.__init__(self, code, description, regular, maximum)

    def improvement_roll(self, count: int = 1):
        """
        Perform an improvement roll
        To make an EDU improvement check, simply roll percentage dice.
        If the result is greater than your present EDU add 1D10 percentage points to your EDU characteristic (note
        that EDU cannot go above 99).
        :return:
        """
        pass


class Investigator:
    """
    COC investigator
    """

    def __init__(self, firstname: str, surname: str, gender: Gender, occupation: str, birthplace: str, residence: str, age: int):
        self.firstname = firstname
        self.surname = surname
        self.gender = gender
        self.age = age
        self.occupation = occupation
        self.birthplace = birthplace
        self.residence = residence
        self.chars = {STR: Characteristic(STR, "Strength", 5 * Roll("3D6").roll(), maximum=99),
                      CON: Characteristic(CON, "Constitution", 5 * Roll("3D6").roll(), maximum=99),
                      SIZ: Characteristic(SIZ, "Size", 5 * Roll("2D6+6").roll(), maximum=200),
                      DEX: Characteristic(DEX, "Dexterity", 5 * Roll("3D6").roll(), maximum=99),
                      APP: Characteristic(APP, "Appearance", 5 * Roll("3D6").roll(), maximum=99),
                      INT: Characteristic(INT, "Intelligence", 5 * Roll("2D6+6").roll(), maximum=99),
                      POW: Characteristic(SIZ, "Power", 5 * Roll("3D6").roll(), maximum=200),
                      EDU: Characteristic(EDU, "Education", 5 * Roll("2D6+6").roll(), maximum=99),
                      LUCK: Characteristic(LUCK, "Luck", 5 * Roll("3D6").roll(), maximum=9999)}
        self.age_impact()
        self.damage_bonus = ""
        self.build = None
        self.set_damage_bonus_and_build()
        self.hit_max = (self.constitution + self.size) // 10
        self.movement = None
        self.set_movement()
        self.occupation_impact()

        # self.possessive_p = gender.POSSESSIVE_PRONOUN[gender]
        # self.object_p = gender.OBJECT_PRONOUN[gender]
        # self.personal_p = PERSONAL_PRONOUN[gender]

    def __repr__(self):
        ret = f"{self.firstname} {self.surname} is a {self.age} year old {self.gender.person()} born in {self.birthplace} and living in {self.residence}. At the moment {self.gender.personal()} is a {self.occupation}"
        return ret

    def occupation_impact(self) -> None:
        """
        Change the skills based on the occupation
        """
        pass

    def set_damage_bonus_and_build(self) -> None:
        """
        Set damage bonus and build
        """
        strength_and_size = self.strength + self.size

        if strength_and_size < 65:
            t = ["-2", -2]
        elif strength_and_size < 85:
            t = ["-1", -1]
        elif strength_and_size < 125:
            t = ["0", -0]
        elif strength_and_size < 165:
            t = ["D4", -1]
        elif strength_and_size < 205:
            t = ["D6", -1]
        else:
            raise ValueError(f"SIZ + STR  ({strength_and_size}) > 204")
        self.damage_bonus, self.build = t

    def set_movement(self) -> None:
        """
        Set movement
        """
        if self.dexterity < self.size and self.strength < self.size:
            self.movement = 7
        elif self.dexterity > self.size and self.strength > self.size:
            self.movement = 9
        else:
            self.movement = 8

        age_term = max(0, (self.age // 10) - 3)
        self.movement += age_term

    def _get_char_value(self, code: str) -> int:
        return self.chars[code].regular

    def _set_char_value(self, code: str, new_value: int):
        self.chars[code].regular = new_value

    @property
    def strength(self):
        """
        STR getter
        :return: STR
        """
        return self._get_char_value(STR)

    @strength.setter
    def strength(self, new_value: int):
        """
        STR setter
        :param new_value: new STR value
        """
        self._set_char_value(STR, new_value)

    @property
    def constitution(self):
        """
        CON getter
        :return: CON
        """
        return self._get_char_value(CON)

    @constitution.setter
    def constitution(self, new_value: int):
        """
        CON setter
        :param new_value: new CON value
        """
        self._set_char_value(CON, new_value)

    @property
    def size(self):
        """
        SIZ getter
        :return: SIZ
        """
        return self._get_char_value(SIZ)

    @size.setter
    def size(self, new_value: int):
        """
        SIZ setter
        :param new_value: new SIZ value
        """
        self._set_char_value(SIZ, new_value)

    @property
    def dexterity(self):
        """
        DEX getter
        :return: DEX
        """
        return self._get_char_value(DEX)

    @dexterity.setter
    def dexterity(self, new_value: int):
        """
        DEX setter
        :param new_value: new DEX value
        """
        self._set_char_value(DEX, new_value)

    @property
    def appearance(self):
        """
        APP getter
        :return: APP
        """
        return self._get_char_value(APP)

    @appearance.setter
    def appearance(self, new_value: int):
        """
        APP setter
        :param new_value: new APP value
        """
        self._set_char_value(APP, new_value)

    @property
    def intelligence(self):
        """
        INT getter
        :return: INT
        """
        return self._get_char_value(INT)

    @intelligence.setter
    def intelligence(self, new_value: int):
        """
        APP setter
        :param new_value: new INT value
        """
        self._set_char_value(INT, new_value)

    @property
    def power(self):
        """
        POW getter
        :return: POW
        """
        return self._get_char_value(POW)

    @power.setter
    def power(self, new_value: int):
        """
        POW setter
        :param new_value: new POW value
        """
        self._set_char_value(POW, new_value)

    @property
    def education(self):
        """
        EDU getter
        :return: EDU
        """
        return self._get_char_value(EDU)

    @education.setter
    def education(self, new_value: int):
        """
        EDU setter
        :param new_value: new EDU value
        """
        self._set_char_value(EDU, new_value)

    def generate_name(self, gender: Gender = None) -> (str, str, Gender):
        """
        Generate a random
        :param gender:
        :return:
        """
        raise NotImplementedError()

    def education_improvement(self) -> None:
        """
        Perform a EDU improvement
        """
        pass

    def deduct(self, amount: int, *args) -> None:
        """
        Deduct the amount spread over the provided attributes
        :param amount: amount to spread
        :param args: attributes to deduct the amount from
        """
        spread = Roll.spread(amount, len(args))
        for i in range(len(spread)):
            self.chars[args[i]].deduct(spread[i])

    def age_impact(self):
        """
        AGE modifiers:
        A player can choose any age between 15 and 90 for their
        investigator. If you wish to create an investigator outside
        this age range, it is up to the Keeper to adjudicate. Use the
        appropriate modifier for your chosen age only (they are not
        cumulative).
        """
        if self.age < 20:
            LOGGER.info("Age is below 20.")
            LOGGER.info("Deduct 5 points among STR and SIZ.")
            self.deduct(5, STR, SIZ)
            LOGGER.info("Deduct 5 points from EDU.")
            self.education -= 5
            LOGGER.info("Roll twice to generate a Luck score and use the higher value")
            self.chars[LUCK].set_if_higher(5 * Roll("3D6").roll())
        elif self.age < 40:
            self.chars[EDU].improvement_roll()
        elif self.age < 50:
            self.chars[EDU].improvement_roll(2)
            self.deduct(5, STR, CON, DEX)
            self.appearance -= 5
        elif self.age < 60:
            """
            50s: Make 3 improvement checks for EDU 
            and deduct 10 points among STR, CON or DEX, 
            and reduce APP by 10.
            """
            self.chars[EDU].improvement_roll(3)
            self.deduct(10, STR, CON, DEX)
            self.appearance -= 10
        elif self.age < 70:
            """
            60s: Make 4 improvement checks for EDU
            and deduct 20 points among STR, CON or DEX, 
            and reduce APP by 15.
            """
            self.chars[EDU].improvement_roll(4)
            self.deduct(20, STR, CON, DEX)
            self.appearance -= 15
        elif self.age < 80:
            """
            70s: Make 4 improvement checks for EDU 
            and deduct 40 points among STR, CON or DEX, 
            and reduce APP by 20.
            """
            self.chars[EDU].improvement_roll(4)
            self.deduct(40, STR, CON, DEX)
            self.appearance -= 20
        else:
            """
            80s: Make 4 improvement checks for EDU 
            and deduct 80 points among STR, CON or DEX, 
            and reduce APP by 25.
            """
            self.chars[EDU].improvement_roll(4)
            self.deduct(80, STR, CON, DEX)
            self.appearance -= 25


me = Investigator(firstname="Jessy",
                  surname="Williams",
                  gender=Gender.FEMALE,
                  birthplace="Boston",
                  residence="Arkham",
                  occupation="Writer",
                  age=17)

if __name__ == "__main__":
    r = Roll("D6").roll()
    LOGGER.debug(Roll.spread(-21, 4))
    LOGGER.debug(Roll.spread(-21, 4))
