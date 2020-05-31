from typing import Dict, List, Any


def map_schedule_weekday_keys_to_idx(schedule: Dict[str, List]) -> (Dict[int, Any], List[str]):
    d = {}
    weekdays = []
    for i, weekday in enumerate(schedule):
        d[i] = schedule[weekday]
        weekdays.append(weekday)
    return d, weekdays


def map_schedule_idx_keys_to_weekdays(schedule: Dict[int, List], weekday_keys: List[str]) -> Dict[str, Any]:
    d = {}
    for idx in schedule.keys():
        d[weekday_keys[idx]] = schedule[idx]
    return d


def capitalize_keys(data: Dict[str, Any]) -> Dict[str, Any]:
    d = {}
    for k, v in data.items():
        d[k.capitalize()] = v
    return d


def flatten_dict_values(data: Dict[int, Any]) -> Dict[int, Any]:
    d = {}
    for k, v in data.items():
        value_as_string = ", ".join(v)
        d[k] = value_as_string
    return d
