import unittest
import json

from src.opening_hours import format_opening_hours


class FormatOpeningHoursTestCase(unittest.TestCase):
    def test_capitalize_days(self):
        data = {
            "monday": [
                {
                    "type": "open",
                    "value": 36000
                },
                {
                    "type": "close",
                    "value": 64800
                }
            ]
        }
        formatted = format_opening_hours(data)
        self.assertIn("Monday", formatted)

    def test_empty_day_is_closed(self):
        data = {
            "monday": []
        }
        formatted = format_opening_hours(data)
        self.assertEqual("Closed", formatted["Monday"])

    def test_opening_and_closing_time(self):
        data = {
            "monday": [
                {
                    "type": "open",
                    "value": 43200
                },
                {
                    "type": "close",
                    "value": 75600
                }
            ],
            "tuesday": [
                {
                    "type": "open",
                    "value": 36000
                },
                {
                    "type": "close",
                    "value": 64800
                }
            ],
        }
        formatted = format_opening_hours(data)
        self.assertEqual("12 PM - 9 PM", formatted["Monday"])
        self.assertEqual("10 AM - 6 PM", formatted["Tuesday"])


if __name__ == '__main__':
    unittest.main()
