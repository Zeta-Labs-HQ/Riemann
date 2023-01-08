import re
from datetime import datetime
from typing import Optional

from dateutil.relativedelta import relativedelta

TIME_REGEX = re.compile(
    # years
    r"(?P<years>\d+)(?:y|yr|yrs|year|years)?"
    # months
    r"(?P<months>\d+)(?:mon|month|months)?"
    # days
    r"(?P<days>\d+)(?:d|day|days)?"
    # hours
    r"(?P<hours>\d+)(?:h|hr|hrs|hour|hours)?"
    # minutes
    r"(?P<minutes>\d+)(?:m|min|mins|minute|minutes)?"
    # seconds
    r"(?P<seconds>\d+)(?:s|sec|secs|second|seconds)?"
    # milliseconds
    r"(?P<milliseconds>\d+)(?:ms|millis|millisec|millisecs|millisecond|milliseconds)?",
    re.IGNORECASE,
)


def parse_time(time_str: str) -> relativedelta:
    """Parse a time string into a relativedelta object.

    Parameters
    ----------
    time_str : str
        The time string to parse.

    Returns
    -------
    relativedelta
        The parsed time string.

    Raises
    ------
    ValueError
        If the time string is invalid.
    """
    match = TIME_REGEX.match(time_str)

    if not match:
        raise ValueError(f"Invalid time string: {time_str}")

    time_dict = {k: int(v) for k, v in match.groupdict(default=0).items()}
    return relativedelta(**time_dict)


def humanize_time(time_delta: relativedelta, min_unit: str = "seconds") -> str:
    """Convert a relative delta into human readable time."""
    time_dict = {
        "years": time_delta.years,
        "months": time_delta.months,
        "weeks": time_delta.weeks,
        "days": time_delta.days,
        "hours": time_delta.hours,
        "minutes": time_delta.minutes,
        "seconds": time_delta.seconds,
        "microseconds": time_delta.microseconds,
    }

    time_list = []

    for unit, value in time_dict.items():
        if value:
            time_list.append(f"{value} {unit if value != 1 else unit[:-1]}")

        if unit == min_unit:
            break

    if len(time_list) > 1:
        time_str = " ".join(time_list[:-1])
        time_str += f" and {time_list[-1]}"
    elif len(time_list) == 0:
        time_str = "now"
    else:
        time_str = time_list[0]

    return time_str


def time_ago(
    _from: datetime, to: Optional[datetime] = None, min_unit: str = "seconds"
) -> str:
    if not to:
        to = datetime.utcnow()

    time_delta = relativedelta(to, _from)
    return f"{humanize_time(time_delta, min_unit=min_unit)} ago."
