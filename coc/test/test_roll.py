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

import math
import unittest

from coc.core.roll import Die, Roll


class MyTestCase(unittest.TestCase):
    def test_die(self):
        # wrong parameter values
        self.assertRaises(TypeError, Die, 0)
        self.assertRaises(TypeError, Die, 0.2)
        self.assertRaises(TypeError, Die, -2)
        self.assertRaises(TypeError, Die, "EEE")

        # 1 sided die only rolls 1
        die = Die(1)
        self.assertEqual(1, die.sides)
        for _ in range(100):
            self.assertEqual(1, die.sides)

        # Roll D1 to D100 many times
        for number in range(100):
            count = number + 1
            buckets = [0] * count
            die = Die(count)
            for i in range(count * 1000):
                res = die.value() - 1
                buckets[res] += 1
            # check that every value appears a lot of time
            for i in range(count):
                self.assertTrue(buckets[i] > 800)

    def test_spread(self):
        rang = 100
        for i in range(rang):
            for j in range(rang):
                value = i - rang // 2
                res = Roll.spread(value, j + 1)
                self.assertEqual(j + 1, len(res))
                self.assertEqual(value, sum(res))
                for k in range(j + 1):
                    if value < 0:
                        self.assertTrue(res[k] <= 0)
                    else:
                        self.assertTrue(res[k] >= 0)

    def test_zz(self):
        count = 10000000
        sequence_max = min(max(2, int(math.log10(count) - 2)), 6)
        seq = ""
        die = Roll('D6')
        d = dict()
        s = dict()
        for _ in range(count):
            roll = die.roll()
            """
            tel frequentie van waarde
            """
            count = d.get(roll, 0)
            count += 1
            d[roll] = count

            """
            tel frequentie van sequenties 
            """
            seq = f"{seq}{roll}"
            if len(seq) < sequence_max:
                continue
            if len(seq) > sequence_max:
                seq = seq[1:]
            count = s.get(seq, 0)
            count += 1
            s[seq] = count

        for x in sorted(d.keys()):
            print(f"{x} : {d[x]} => {d[x] * 100 / count:.2f}%")

        for x in sorted(s.keys()):
            print(f"{x} : {s[x]} => {s[x] * 100 / count:.2f}%")


if __name__ == '__main__':
    unittest.main()
