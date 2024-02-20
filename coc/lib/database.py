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

import csv
import sqlite3
from typing import Optional

from coc import config
from coc.core import roll
from coc.core.gender import Gender
from coc.core.rules import Era
from coc.lib.logger import LOGGER


def get_random_row(file_path: str, where: str = None) -> Optional[tuple]:
    """
    Read a csv into memory
    :param file_path: full path to a csv file
    :param where: where clause for query
    """
    LOGGER.debug(f"Getting a random row fro file {file_path} with criteria: {where}")
    try:
        connection = sqlite3.connect(":memory:")
        cursor = connection.cursor()
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=':')
            headers = next(csvreader)
            cursor.execute(f"CREATE TABLE TABLETABLE ({', '.join(headers)})")
            for line in csvreader:
                cursor.execute(f"INSERT INTO TABLETABLE VALUES ({', '.join(['?' for _ in line])})", line)
        connection.commit()
        query = f"""SELECT * FROM TABLETABLE {'' if where is None else ' WHERE ' + where}"""
        res = cursor.execute(query).fetchall()

        if res is None or len(res) == 0:
            raise Exception()
        rnd = roll.random_func(len(res)) - 1
        return res[rnd]
    except Exception as e:
        LOGGER.error(f"Issue with selecting a row from csv file. => {e}")
    return None


def add_criterium(dbname, value, criteria) -> None:
    """
    If value is not None, then a part of where clause will be added to the criteria lst
    :param dbname: name of the database title
    :param value: the value of the criterium
    :param criteria: list to append to
    """
    if value is None:
        return
    criteria.append(f"{dbname} = '{value}'")


def get_first_name(gender: Gender = None, language: str = None, era: Era = None) -> str:
    """
    Get a random first name
    :param gender: selection criterium 1
    :param language:  selection criterium 2
    :param era: selection criterium 3
    :return: str
    """
    criteria = []
    add_criterium('GENDER', None if gender is None else Gender.short_code(gender), criteria)
    add_criterium('LANG', language, criteria)
    add_criterium('ERA', era, criteria)
    where = f"{' AND '.join(criteria)}" if len(criteria) > 0 else None
    return get_random_row(config.CSV_FIRST_NAMES, where=where)[0]


def get_last_name(language: str = None, era: Era = None) -> str:
    """
    Get a random last name
    :param language:  selection criterium 2
    :param era: selection criterium 3
    :return: str
    """
    criteria = []
    add_criterium('LANG', language, criteria)
    add_criterium('ERA', era, criteria)
    where = f"{' AND '.join(criteria)}" if len(criteria) > 0 else None
    return get_random_row(config.CSV_NAMES, where=where)[0]


if __name__ == "__main__":
    for _ in range(1000):
        print(get_first_name(gender=Gender.FEMALE) + ' ' + get_last_name(language='NL') )

    # raise NotImplementedError(__file__)
