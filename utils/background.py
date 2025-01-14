import time

from fastapi import BackgroundTasks
from datetime import datetime
# 定义通用后台任务
async def write_log(message:str):
    # time.sleep(5)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('log.txt', 'a') as log_file:
        log_file.write(f'{message} {current_time}\n')

# 定义后台任务依赖
def log_dependency(background_tasks: BackgroundTasks,log_message:str = "新增后台异步写日志任务"):
    background_tasks.add_task(write_log, log_message)
    return "写日志任务已经创建"