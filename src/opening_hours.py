from typing import Dict, List, Any

from src.dict_utils import map_schedule_weekday_keys_to_idx, map_schedule_idx_keys_to_weekdays, capitalize_keys, \
    flatten_dict_values
from src.format_utils import format_timestamps, format_opening_time


def mark_empty_days_closed(data: Dict[str, Any]) -> Dict[str, Any]:
    d = {}
    for k, v in data.items():
        if len(v) == 0:
            d[k] = "Closed"
        else:
            d[k] = v
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
                        opening_hour_str = format_opening_time(opening_time=opening["value"],
                                                               closing_time=next_opening["value"])
                        opening_hours.append(opening_hour_str)
                else:
                    if schedule_idx + 1 < len(formatted_schedule):
                        next_day = formatted_schedule[schedule_idx + 1]
                        next_day_first_opening = next_day[0]
                        if next_day_first_opening["type"] == "close":
                            opening_hour_str = format_opening_time(opening_time=opening["value"],
                                                                   closing_time=next_day_first_opening["value"])
                            opening_hours.append(opening_hour_str)
                    else:
                        next_day = formatted_schedule[0]
                        next_day_first_opening = next_day[0]
                        if next_day_first_opening["type"] == "close":
                            opening_hour_str = format_opening_time(opening_time=opening["value"],
                                                                   closing_time=next_day_first_opening["value"])
                            opening_hours.append(opening_hour_str)

        d[schedule_idx] = opening_hours

    opening_schedules_as_string = flatten_dict_values(d)
    return opening_schedules_as_string


def format_opening_hours(data: Dict[str, List]) -> Dict[str, Any]:
    schedule_with_int_keys, weekday_keys = map_schedule_weekday_keys_to_idx(data)
    with_opening_hours = set_opening_and_closing_time(schedule_with_int_keys)
    schedule_with_weekday_keys = map_schedule_idx_keys_to_weekdays(with_opening_hours,
                                                                   weekday_keys)
    with_closed_days = mark_empty_days_closed(schedule_with_weekday_keys)
    with_capitalized_days = capitalize_keys(with_closed_days)
    return with_capitalized_days
