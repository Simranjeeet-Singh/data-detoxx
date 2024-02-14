from datetime import datetime, timezone

def convert_to_utc(datetime_str: str) -> str:
    """
    Convert a date-time string to a UTC format string.

    Args:
        datetime_str (str): A string representing date and time in the format 'YYYY-MM-DD HH:MM:SS.SSS'.

    Returns:
        str: A string representing date and time in UTC format 'YYYY-MM-DDTHHMMSS.SSSZ'.
    """
    # Convert string to datetime object
    dt_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S.%f')


    # Convert datetime object to UTC format string without colons and period
    utc_format_str = dt_obj.strftime('%Y-%m-%dT%H%M%S%f')[:-3] + 'Z'

    return utc_format_str

# Example usage
datetime_str = '2022-11-03 14:20:49.962'
utc_format_str = convert_to_utc(datetime_str)
print(utc_format_str)




from datetime import datetime

def convert_from_utc(utc_format_str: str) -> str:
    """
    Convert a UTC format string to the date-time format 'YYYY-MM-DD HH:MM:SS.SSS'.

    Args:
        utc_format_str (str): A string representing date and time in UTC format 'YYYY-MM-DDTHHMMSS.SSSZ'.

    Returns:
        str: A string representing date and time in the format 'YYYY-MM-DD HH:MM:SS.SSS'.
    """
    # Convert string to datetime object
    dt_obj = datetime.strptime(utc_format_str, '%Y-%m-%dT%H%M%S%fZ')

    # Convert datetime object to the desired format string
    desired_format_str = dt_obj.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    return desired_format_str

# Example usage
utc_format_str = '2022-11-03T142049962Z'
datetime_str = convert_from_utc(utc_format_str)
print('objective: 2022-11-03 14:20:49.962', datetime_str)
