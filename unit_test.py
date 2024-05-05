import unittest
from main import particle_oob_check
from main import change_of_state


class MyTestCase(unittest.TestCase):
    def test_particle_oob_check(self):
        function = particle_oob_check(25, 25, 50, 50)
        self.assertEqual(function, True)

        function = particle_oob_check(0, 0, 50, 50)
        self.assertEqual(function, True)

        function = particle_oob_check(0, 0, 49, 49)
        self.assertEqual(function, True)

        function = particle_oob_check(50, 50, 50, 50)
        self.assertEqual(function, False)

        function = particle_oob_check(0, 50, 50, 50)
        self.assertEqual(function, False)

        function = particle_oob_check(50, 0, 50, 50)
        self.assertEqual(function, False)

    def test_change_of_state(self):
        function = change_of_state(25, 25)
        self.assertEqual(function, False)

if __name__ == '__main__':
    unittest.main()
