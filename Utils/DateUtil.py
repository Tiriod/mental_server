"""
Program Name: mental_server
File Name: DateUtil
Author: TIMEME
Create Time: 2023/11/18 10:00
"""
from datetime import datetime, timedelta


def get_next_image_id():
    # 获取当前日期和时间
    now = datetime.now()
    # 构建 image_id 前缀
    prefix = now.strftime("%Y%m%d")
    # 读取保存自增 ID 的文件
    try:
        with open("image_id.txt", "r") as file:
            last_id, last_date = file.read().split(",")
            last_date = datetime.strptime(last_date, "%Y-%m-%d")
    except FileNotFoundError:
        # 如果文件不存在，重置 ID
        last_id = "0000"
        last_date = now - timedelta(days=1)

    # 如果已经到达新的一天，重置 ID
    if now.date() > last_date.date():
        last_id = "0000"

    # 增加自增 ID
    next_id = str(int(last_id) + 1).zfill(4)

    # 保存当前 ID 和日期到文件
    with open("image_id.txt", "w") as file:
        file.write(f"{next_id},{now.date()}")

    # 返回完整的 image_id
    return prefix + next_id
