"""
Converting swim times between (m)m:ss.hh text and seconds.
"""

def timeToSec(swim_time):
    """
    Converts a swimming time in (m)m:ss.hh format to total seconds.
    :param swim_time: str - Time in the format 'mm:ss.hh' or 'ss.hh'
    :return: float - Time in seconds
    """
    if ("M" in swim_time):
        swim_time = swim_time.replace('M', '')

    if ':' in swim_time:
        # If the time includes minutes
        minutes, seconds = swim_time.split(':')
        total_seconds = int(minutes) * 60 + float(seconds)
    else:
        # If the time is only in seconds
        total_seconds = float(swim_time)
    return round(total_seconds, 2)

def secToTime(seconds):
    """
    Converts time in total seconds to (m)m:ss.hh format.
    If the input time is less than 60 seconds, it remains in ss.hh format.
    :param seconds: float - Time in seconds
    :return: str - Time in the format 'mm:ss.hh' or 'ss.hh'
    """
    if seconds < 60:
        # If the total time is less than one minute, keep it in seconds format
        return f"{seconds:.2f}"
    else:
        # Otherwise, convert to mm:ss.hh
        minutes = int(seconds // 60)
        remaining_seconds = seconds % 60
        return f"{minutes}:{remaining_seconds:05.2f}"
