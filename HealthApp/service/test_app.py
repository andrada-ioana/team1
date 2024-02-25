from unittest import TestCase
import interpret_data

class TestApp(TestCase):
    def test_app(self):
        self.assertEqual(interpret_data.calculate_nutritional_score(["apple", "banana"], {"apple": {"Calories": 100}, "banana": {"Calories": 200}}), 300)