__author__ = 'sunwj'

"checkin logs are small files which will take lots of inode space."


import subprocess


def archive_logs():

    path = "/home/"
    subprocess.call("ls -l  "+path,shell=True)

def get_last_month():
    from datetime import datetime
    now_time = datetime.now()
    this_month = now_time.month

    last_month = now_time.replace(month=this_month-1)



