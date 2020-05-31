from datetime import datetime, timezone
from typing import Dict, List, Any


def format_time(timestamp: int) -> (int, int):
    time = datetime.fromtimestamp(timestamp, timezone.utc)
    if time.minute == 0:
        return time.strftime("%-I %p")
    else:
        return time.strftime("%-I.%M %p")


def mark_empty_days_closed(data: Dict[str, Any]) -> Dict[str, Any]:
    d = {}
    for k, v in data.items():
        if len(v) == 0:
            d[k] = "Closed"
        else:
            d[k] = v
    return d


def format_timestamps(data: Dict[str, Any]) -> Dict[str, Any]:
    d = {}
    for weekday, opening_times in data.items():
        opening_and_closing_times = []
        for opening_time in opening_times:
            timestamp = opening_time["value"]
            formatted_time = format_time(timestamp)
            opening_and_closing_times.append(
                {
                    "type": opening_time["type"],
                    "value": formatted_time
                }
            )
        d[weekday] = opening_and_closing_times
    return d


def flatten_hours(data: Dict[str, Any]) -> Dict[str, Any]:
    d = {}
    for k, v in data.items():
        opening_hours_as_string = ",".join(v)
        d[k] = opening_hours_as_string
    return d


def set_opening_and_closing_time(data: Dict[str, Any]) -> Dict[str, Any]:
    formatted_schedule = format_timestamps(data)
    schedule_iter = iter(formatted_schedule)
    for weekday in schedule_iter:
        opening_hours = []
        opening_hours_iter = iter(formatted_schedule[weekday])
        for opening in opening_hours_iter:
            next_opening = next(opening_hours_iter)
            if opening["type"] == "open" and next_opening["type"] == "close":
                opening_hour = opening["value"] + " - " + next_opening["value"]
                opening_hours.append(opening_hour)
        formatted_schedule[weekday] = opening_hours

    opening_schedules_as_strings = flatten_hours(formatted_schedule)
    return opening_schedules_as_strings


def capitalize_weekdays(data: Dict[str, Any]) -> Dict[str, Any]:
    d = {}
    for k, v in data.items():
        d[k.capitalize()] = v
    return d


def format_opening_hours(data: Dict[str, List]) -> Dict[str, Any]:
    with_opening_hours = set_opening_and_closing_time(data)
    with_closed_days = mark_empty_days_closed(with_opening_hours)
    with_capitalized_days = capitalize_weekdays(with_closed_days)
    return with_capitalized_days
