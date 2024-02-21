from datetime import datetime
import calendar


def extract_date(timestamp: str) -> dict:
    """
    Convert a timpetamp into a dictionary with useful key-value pairs

    Parameters:
    - timestamp (str): A timestamp string in the format 'YYYY-MM-DD HH:MM:SS.sss'

    Returns:
    - dict: A dictionary containing the following keys:
        - year [int]
        - month [int]
        - day [int]
        - day_of_week [int] (Mon = 0, Tue = 1 etc.)
        - day_name [varchar]
        - month_name [varchar]
        - quarter [int]
    """

    dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")

    print(dt)

    return {'year': dt.year,
            'month': dt.month,
            'day': dt.day,
            'day_of_week': dt.weekday(),
            'day_name': calendar.day_name[dt.weekday()],
            'month_name': calendar.month_name[dt.month],
            'quarter': (dt.month - 1) // 3 + 1}
