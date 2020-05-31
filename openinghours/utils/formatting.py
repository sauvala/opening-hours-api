from datetime import datetime, timezone
from typing import Dict, Any


def format_time(timestamp: int) -> (int, int):
    time = datetime.fromtimestamp(timestamp, timezone.utc)
    if time.minute == 0:
        return time.strftime("%-I %p")
    else:
        return time.strftime("%-I.%M %p")


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


def format_opening_time(opening_time: str, closing_time: str) -> str:
    return f"{opening_time} - {closing_time}"