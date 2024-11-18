import datetime
import pytz

def string2datetime(string: str):
    """
    Input:
        string: str, on the hour:minute format
    
    Ouput:
        time_of_day: int, time of day in datetime format
    """

    string_hour, string_minute = string.split(":")
    time_of_day = datetime.time(int(string_hour), int(string_minute), 0)

    return time_of_day

def pytz2datetime(timezone):
    pytz_now = datetime.datetime.now(timezone)
    utc_offset = pytz_now.utcoffset()
    datetime_timezone = datetime.timezone(utc_offset)

    return datetime_timezone

def roundHalfHour(dt: datetime.datetime):
    # Get the current minute
    minute = dt.minute

    # Calculate how many minutes to the closest half-hour (either 0 or 30)
    if minute < 15:
        new_minute = 0
    elif minute < 45:
        new_minute = 30
    else:
        new_minute = 0
        dt += datetime.timedelta(hours=1)  # Round up to the next hour if it's closer

    # Create a new datetime with the rounded minute
    return dt.replace(minute=new_minute, second=0, microsecond=0)


    