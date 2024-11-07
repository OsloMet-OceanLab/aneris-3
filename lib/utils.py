import datetime

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