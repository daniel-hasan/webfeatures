import unittest
from feature.preprocessing import PreprocessingMethod, StopWordRemoval

class TestPreprocessingMethod(unittest.TestCase):
    
    def testStopWordRemoval(self):
         text = "The beautiful book is on the black table. I like the book more than everything."
         obj = StopWordRemoval(PreprocessingMethod())
         result = obj.run(text,'english')
         self.assertEqual(text, "beautiful book black table . I like book everything .",
                           "O texto não foi preprocessado corretamente")
    
if __name__=="__main__":
    unittest.main()