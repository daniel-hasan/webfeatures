import unittest
from cmd_line_interface.CaracterInterface import *

class Testa_funcao_imprimirFeatures(unittest.TestCase):
    def test_imprimirFeatures(self):
        obj = CaracterInterface()
        self.assertNotEqual([], obj.imprimirFeatures(), "O vetor retornado esta vazio")

if __name__ == "__main__":
    unittest.main()
