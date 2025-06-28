import datetime
import re


def format_time(time) -> str | None:
    """
    Format a time in seconds to a string in the format HH:MM:SS.
    """
    if time is None:
        return None
    temp = '--:--:--'
    if not isinstance(time, str):
        temp = datetime.timedelta(seconds=float(time))
    temp = re.sub(r'^0:', '', str(temp))
    format_list = temp.split(':')
    duration = ':'.join([f.zfill(2) for f in format_list])
    return duration