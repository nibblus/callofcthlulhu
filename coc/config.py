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
from pathlib import Path

DIR_ROOT = Path("E:\\STACK\\Dev\\callofcthlulhu")

DIR_DATA = Path.joinpath(DIR_ROOT, "data")

CSV_FIRST_NAMES = Path.joinpath(DIR_DATA,"first_names.csv")
CSV_NAMES = Path.joinpath(DIR_DATA, "names.csv")
CSV_OCCUPATIONS = Path.joinpath(DIR_DATA, "occupations")
CSV_SKILLS = Path.joinpath(DIR_DATA, "skills")

if __name__ == "__name__":
    raise NotImplementedError()
