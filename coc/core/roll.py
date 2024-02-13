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

import random
import re

from coc.lib.logger import LOGGER


def random_func(limit: int) -> int:
    """
    Generate a random integer between 1 and limit.
    This function is the heart of the die rolls.
    If you don't trust its randomness, then feel free to replace it.
    :param limit: upper bound
    :return: random number between 1 and limit
    """
    if not isinstance(limit, int) or limit < 1:
        raise TypeError(f"parameter limit must be integer greater than 0:  {limit}")
    return random.randint(1, limit)


class Die:
    """
    A die
    """

    def __init__(self, sides: int):
        if not isinstance(sides, int) or sides < 1:
            raise TypeError(f"Sides {sides} must be strict positive integer")
        self.sides = sides
        self._value = None

    def __repr__(self):
        return f"D{self.sides}"

    def value(self) -> int:
        """
        Generate a number for the die
        :return: Random roll
        """
        self._value = random_func(self.sides)
        return self._value


class Roll:
    """
    Representation of dice roll
    """

    def __init__(self, description: str = "D100"):
        LOGGER.debug(description)
        self.description = description
        self.dice = []
        description = description.replace("-", "|-").replace("+", "|")
        terms = re.split(r'\|', description)
        terms = [term.split("D") for term in terms]
        for term in terms:
            if len(term) == 1:
                if term[0] == '':
                    continue
                self.dice.append(Value(int(term[0])))
            elif len(term) == 2:
                length = 1 if len(term[0]) == 0 else int(term[0])
                for i in range(length):
                    self.dice.append(Die(int(term[1])))

    def roll(self) -> int:
        """
        Roll the die
        :return: random side of the die
        """
        total = 0
        for die in self.dice:
            r = die.value()
            total += r
            LOGGER.debug(f"Rolling {die} => value {r}  (subtotal: {total})")
        return total

    @staticmethod
    def spread(value: int, size: int) -> list:
        """
        Spread a value among and number of variables.
        Spread(10,3) will generate a random list of numbers of length 3, where the sum of all numbers is 10, e.g. [1,7,2]
        :param value: The value to spread
        :param size: the number of values to spread the value among.
        :return: list of variables
        """
        LOGGER.debug(f"Spreading {value} over {size} buckets")
        if not isinstance(size, int) or size < 1:
            raise TypeError(f"parameter limit must be integer greater than 0:  {size}")
        ret = [0] * size
        term = 1
        if value < 0:
            value = - value
            term = -1

        for _ in range(value):
            index = random.randint(0, size - 1)
            ret[index] += term
        return ret


class Value:
    """
    Representation of a value
    """

    def __init__(self, value: int = 1):
        self._value = value

    def __repr__(self):
        return f"Value({self._value})"

    def value(self) -> int:
        """

        :return:
        """
        return self._value


D3 = Roll("D3")
D4 = Roll("D4")
D5 = Roll("D5")
D6 = Roll("D6")
D8 = Roll("D8")
D10 = Roll("D10")
D100 = Roll("D100")

if __name__ == "__main__":
    raise NotImplementedError(__file__)
