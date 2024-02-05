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

from enum import Enum, unique
from typing import Optional

from coc.core import roll


@unique
class Era(Enum):
    """
    COC ERA
    """
    NineteenTwenty = 1
    Modern = 2
    Pulp = 3


class Attribute:
    """
    Value
    """

    def __init__(self, description: str, code: str, regular: int = None):
        self.description = description
        self.code = code
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
    def regular(self, regular: int):
        self._regular = regular
        self._half = regular // 2
        self._fifth = regular // 5

    @staticmethod
    def _compare(value: int, limit: Optional[int]) -> bool:
        """
        Verify if a value is lower than a limit. If no value is provided a random(100) will be generated
        :param value:  Value or None. In case of None a random value wil lbe generated.
        :param limit: Upper limit
        :return: True if value is less than or equal to limit.
        """
        if value is None:
            value = roll.random_func(100)
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


STR = "STR"
CON = "CON"
DEX = "DEX"
SIZ = "SIZ"
APP = "APP"
INT = "INT"
POW = "POW"
EDU = "EDU"


@unique
class Gender(Enum):
    """
    Sex
    """
    MALE = 1
    FEMALE = 2
    X = 3

    def person(self):
        if self == Gender.FEMALE:
            return "woman"
        elif self == Gender.MALE:
            return "man"
        return "X"

    def personal(self):
        if self == Gender.FEMALE:
            return "she"
        elif self == Gender.MALE:
            return "he"
        return "X"


POSSESSIVE_PRONOUN = {
    Gender.MALE: "his",
    Gender.FEMALE: "her",
    Gender.X: "theirs"
}

OBJECT_PRONOUN = {
    Gender.MALE: "him",
    Gender.FEMALE: "her",
    Gender.X: "them"
}

PERSONAL_PRONOUN = {
    Gender.MALE: "he",
    Gender.FEMALE: "she",
    Gender.X: "they"
}


class Characteristic(Attribute):
    """
    Investigator characteristic
    """

    def __init__(self, code, description, regular):
        Attribute.__init__(self, code, description, regular)


class Investigator:
    """
    COC investigator
    """

    def __init__(self, firstname: str, surname: str, gender: Gender, occupation: str, birthplace: str, residence: str, age: int):
        self.firstname = firstname
        self.surname = surname
        self.gender = gender
        self.age = age
        self.possessive_p = POSSESSIVE_PRONOUN[gender]
        self.object_p = OBJECT_PRONOUN[gender]
        self.personal_p = PERSONAL_PRONOUN[gender]
        self.occupation = occupation
        self.birthplace = birthplace
        self.residence = residence
        self.strength = None
        self.constitution = None
        self.dexterity = None
        self.intelligence = None
        self.size = None
        self.power = None
        self.appearance = None
        self.education = None

    def __repr__(self):
        ret = f"{self.firstname} {self.surname} is a {self.age} year old {self.gender.person()} born in {self.birthplace} and living in {self.residence}. At the moment {self.gender.personal()} is a {self.occupation}"
        return ret

    @staticmethod
    def value_or_roll(description, key, **kwargs):
        ret = kwargs.get(key)
        if ret is None:
            ret = Roll(description).roll()
        return ret

    def generate_name(self, gender: Gender = None) -> (str, str, Gender):
        """
        Generate a random
        :param gender:
        :return:
        """
        raise NotImplementedError()

    def set_characteristic(self, **kwargs):
        """

        :param kwargs:
        """
        self.strength = 5 * self.value_or_roll("3D6", STR, **kwargs)
        self.constitution = 5 * self.value_or_roll("3D6", CON, **kwargs)
        self.dexterity = 5 * self.value_or_roll("3D6", DEX, **kwargs)
        self.appearance = 5 * self.value_or_roll("3D6", APP, **kwargs)
        self.intelligence = 5 * self.value_or_roll("2D6+6", INT, **kwargs)
        self.size = 5 * self.value_or_roll("2D6+6", SIZ, **kwargs)


me = Investigator(firstname="Jessy",
                  surname="Williams",
                  gender=Gender.FEMALE,
                  birthplace="Boston",
                  residence="Arkham",
                  occupation=None,
                  age=20)

me.set_characteristic()
print(me.gender.person())

print(me)
