import unittest

from openinghours.app.opening_hours import format_opening_hours


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

    def test_closing_time_on_next_day(self):
        data = {
            "saturday": [
                {
                    "type": "open",
                    "value": 36000
                },
            ],
            "sunday": [
                {
                    "type": "close",
                    "value": 3600
                },
                {
                    "type": "open",
                    "value": 43200
                },
                {
                    "type": "close",
                    "value": 75600
                }
            ],
        }
        formatted = format_opening_hours(data)
        self.assertEqual("10 AM - 1 AM", formatted["Saturday"])
        self.assertEqual("12 PM - 9 PM", formatted["Sunday"])

    def test_closing_on_monday(self):
        data = {
            "monday": [
                {
                    "type": "close",
                    "value": 3600
                },
                {
                    "type": "open",
                    "value": 36000
                },
                {
                    "type": "close",
                    "value": 64800
                }
            ],
            "sunday": [
                {
                    "type": "open",
                    "value": 43200
                },
            ],
        }
        formatted = format_opening_hours(data)
        self.assertEqual("10 AM - 6 PM", formatted["Monday"])
        self.assertEqual("12 PM - 1 AM", formatted["Sunday"])

    def test_only_having_closing_marks_as_closed(self):
        data = {
            "monday": [
                {
                    "type": "open",
                    "value": 36000
                },
            ],
            "tuesday": [
                {
                    "type": "close",
                    "value": 3600
                },
            ],
            "wednesday": [
                {
                    "type": "open",
                    "value": 43200
                },
                {
                    "type": "close",
                    "value": 75600
                }
            ],
        }
        formatted = format_opening_hours(data)
        self.assertEqual("10 AM - 1 AM", formatted["Monday"])
        self.assertEqual("Closed", formatted["Tuesday"])
        self.assertEqual("12 PM - 9 PM", formatted["Wednesday"])

    def test_open_multiple_times_per_day(self):
        data = {
            "saturday": [
                {
                    "type": "open",
                    "value": 32400
                },
                {
                    "type": "close",
                    "value": 39600
                },
                {
                    "type": "open",
                    "value": 57600
                },
                {
                    "type": "close",
                    "value": 82800
                }
            ],
        }
        formatted = format_opening_hours(data)
        self.assertEqual("9 AM - 11 AM, 4 PM - 11 PM", formatted["Saturday"])

    def test_open_multiple_times_and_closing_time_next_day(self):
        data = {
            "friday": [
                {
                    "type": "open",
                    "value": 64800
                }
            ],
            "saturday": [
                {
                    "type": "close",
                    "value": 3600
                },
                {
                    "type": "open",
                    "value": 32400
                },
                {
                    "type": "close",
                    "value": 39600
                },
                {
                    "type": "open",
                    "value": 57600
                },
                {
                    "type": "close",
                    "value": 82800
                }
            ],
        }
        formatted = format_opening_hours(data)
        self.assertEqual("6 PM - 1 AM", formatted["Friday"])
        self.assertEqual("9 AM - 11 AM, 4 PM - 11 PM", formatted["Saturday"])


if __name__ == '__main__':
    unittest.main()
