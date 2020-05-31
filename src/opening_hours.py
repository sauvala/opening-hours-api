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


def format_timestamps(data: Dict[int, Any]) -> Dict[int, Any]:
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


def flatten_hours(data: Dict[int, Any]) -> Dict[int, Any]:
    d = {}
    for k, v in data.items():
        opening_hours_as_string = ",".join(v)
        d[k] = opening_hours_as_string
    return d


def set_opening_and_closing_time(data: Dict[int, Any]) -> Dict[int, Any]:
    d = {}
    formatted_schedule = format_timestamps(data)
    for schedule_idx in formatted_schedule.keys():
        weekday_openings = formatted_schedule[schedule_idx]
        opening_hours = []
        for opening_idx, opening in enumerate(weekday_openings):

            if opening["type"] == "close":
                continue

            if opening["type"] == "open":
                if opening_idx + 1 < len(weekday_openings):
                    next_opening = weekday_openings[opening_idx + 1]
                    if next_opening["type"] == "close":
                        opening_hour_str = opening["value"] + " - " + next_opening["value"]
                        opening_hours.append(opening_hour_str)
                else:
                    if schedule_idx + 1 < len(formatted_schedule):
                        next_day = formatted_schedule[schedule_idx + 1]
                        next_day_first_opening = next_day[0]
                        if next_day_first_opening["type"] == "close":
                            opening_hour_str = opening["value"] + " - " + next_day_first_opening["value"]
                            opening_hours.append(opening_hour_str)
                    else:
                        next_day = formatted_schedule[0]
                        next_day_first_opening = next_day[0]
                        if next_day_first_opening["type"] == "close":
                            opening_hour_str = opening["value"] + " - " + next_day_first_opening["value"]
                            opening_hours.append(opening_hour_str)

        d[schedule_idx] = opening_hours

    opening_schedules_as_strings = flatten_hours(d)
    return opening_schedules_as_strings


def capitalize_weekdays(data: Dict[str, Any]) -> Dict[str, Any]:
    d = {}
    for k, v in data.items():
        d[k.capitalize()] = v
    return d


def map_schedule_keys_to_numbers(schedule: Dict[str, List]) -> (Dict[int, Any], List[str]):
    d = {}
    weekdays = []
    for i, weekday in enumerate(schedule):
        d[i] = schedule[weekday]
        weekdays.append(weekday)
    return d, weekdays


def map_schedule_keys_to_weekdays(schedule: Dict[int, List], weekday_keys: List[str]) -> Dict[str, Any]:
    d = {}
    for idx in schedule.keys():
        d[weekday_keys[idx]] = schedule[idx]
    return d


def format_opening_hours(data: Dict[str, List]) -> Dict[str, Any]:
    schedule_with_int_keys, weekday_keys = map_schedule_keys_to_numbers(data)
    with_opening_hours = set_opening_and_closing_time(schedule_with_int_keys)
    schedule_with_weekday_keys = map_schedule_keys_to_weekdays(with_opening_hours,
                                                               weekday_keys)
    with_closed_days = mark_empty_days_closed(schedule_with_weekday_keys)
    with_capitalized_days = capitalize_weekdays(with_closed_days)
    return with_capitalized_days
