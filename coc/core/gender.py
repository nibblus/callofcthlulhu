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


@unique
class Gender(Enum):
    """
    Sex
    """
    MALE = 1
    FEMALE = 2
    X = 3

    def person(self):
        """

        :return:
        """
        return NOUN.get(self)

    def personal(self):
        """

        :return:
        """
        return PERSONAL_PRONOUN.get(self)


NOUN = {
    Gender.MALE: "man",
    Gender.FEMALE: "woman",
    Gender.X: "x"

}

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

if __name__ == "__name__":
    raise NotImplementedError()
