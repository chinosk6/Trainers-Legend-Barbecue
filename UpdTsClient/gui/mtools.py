import time


def timestamp_to_text(timestamp: int, _format="%Y-%m-%d %H:%M:%S"):
    if timestamp > 9999999999:
        timestamp = timestamp / 1000
    return time.strftime(_format, time.localtime(timestamp))
