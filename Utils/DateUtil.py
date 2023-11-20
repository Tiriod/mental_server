"""
Program Name: mental_server
File Name: DateUtil
Author: TIMEME
Create Time: 2023/11/18 10:00
"""
from datetime import datetime


# 计算当前时间ID信息
def get_image_id():
    TIME = datetime.now()
    year = TIME.year
    month = TIME.month
    day = TIME.day
    hour = TIME.hour
    minute = TIME.minute
    second = TIME.second
    time_list = [month, day, hour, minute, second]

    def single2double(time):
        if len(str(time)) == 1:
            return "0" + str(time)
        else:
            return str(time)

    res = str(year)
    for time in time_list:
        time_string = single2double(time)
        res += time_string
    return res
