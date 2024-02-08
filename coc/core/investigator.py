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

import logging
from typing import Optional

from coc.core.gender import Gender
from coc.core.roll import Roll, random_func, D6, D100, D10


class Attribute:
    """
    Value
    """

    def __init__(self, description: str, code: str, regular: int = None, maximum: int = 100):
        self.description = description
        self.code = code
        self.maximum = maximum
        self._regular = regular
        self._half = regular // 2
        self._fifth = regular // 5

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
        logging.debug(f"Trying to set {self} to {new_value}")
        if new_value > self.maximum:
            logging.debug(f"{new_value} exceeds maximum of {self.maximum}, so limiting it so maximum")
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

    def is_extreme(self, value: Optional[int]):
        """
        Perform an extreme hard check
        :param value: Value to check, if no value is provided a random(100) will be generated
        :return: True if value is less than or equal to _fifth
        """
        return self._compare(value, self._fifth)

    def deduct(self, value: int):
        """

        :param value:
        :return:
        """
        logging.info(f"Deducting {value} from {self}")
        self.regular -= value

    def set_if_higher(self, value):
        if value > self.regular:
            self.regular = value

    def improvement_roll(self):
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

    def improvement_roll(self):
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
        # self.possessive_p = gender.POSSESSIVE_PRONOUN[gender]
        # self.object_p = gender.OBJECT_PRONOUN[gender]
        # self.personal_p = PERSONAL_PRONOUN[gender]

    def __repr__(self):
        ret = f"{self.firstname} {self.surname} is a {self.age} year old {self.gender.person()} born in {self.birthplace} and living in {self.residence}. At the moment {self.gender.personal()} is a {self.occupation}"
        return ret

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
        """
        pass

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
            logging.info("Age is below 20.")
            logging.info("Deduct 5 points among STR and SIZ.")
            r = D6.roll()
            str_mod = r - 1
            siz_mod = 5 - str_mod
            logging.debug(f"Rolled {str_mod} => {str_mod} is deducted from STR. {siz_mod} from SIZ.")
            self.strength -= str_mod
            self.size -= siz_mod
            logging.info("Deduct 5 points from EDU.")
            self.education -= 5
            logging.info("Roll twice to generate a Luck score and use the higher value")

        elif self.age < 40:
            pass
        elif self.age < 50:
            pass
        elif self.age < 60:
            pass
        elif self.age < 70:
            pass
        elif self.age < 80:
            pass
        else:
            """
            Make 4 improvement checks for EDU and deduct 80 points
            among STR, CON or DEX, and reduce APP by 25
            """
            pass

    def set_characteristic(self):
        self.age_impact()


me = Investigator(firstname="Jessy",
                  surname="Williams",
                  gender=Gender.FEMALE,
                  birthplace="Boston",
                  residence="Arkham",
                  occupation=None,
                  age=17)

me.set_characteristic()
print(me.gender.person())

print(me)