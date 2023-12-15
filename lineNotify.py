# coding=utf-8
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from line_notify import LineNotify

inMac = True

#STOCKS_LINE_NOTIFY_TOKEN="t6SN1yTGZzmwDhsaKoVLD9N0ErS2KKpYS0G8d9EWPXW"
#FUTURES_LINE_NOTIFY_TOKEN = "5rp7cILfzoW1TePtRtIUi6QZVY9fOGNpJAcwtyGH5w3"

WATCH_DIR = ""
dirs = []

if inMac:
    WATCH_DIR = "."
    dirs = [
        {
            'dir': f'{WATCH_DIR}/lineTest',
            'token': "5rp7cILfzoW1TePtRtIUi6QZVY9fOGNpJAcwtyGH5w3" # sean person
        }
    ]
else:
    WATCH_DIR = r'D:\NotifyXQ\files'
    dirs = [
        {
            'dir': f'{WATCH_DIR}\stocks',
            'token': "IlkVWM4IPo9o7Z7kt7akhvrK4zYJup18AC9KgL1VxYv" # 個股
        },
        {
            'dir': f'{WATCH_DIR}\\futures',
            'token': "HsOEsZiDnYLuj0yt5ZHesoocucp4nU1E2aXvNwDkEOz" # 期貨
        },
        {
            'dir': f'{WATCH_DIR}\\free',
            'token': "p4BcmkxHrT0nnxFFzfIIYVTYLt2D1akSBJe8z0b2dNW" # 股期小幫手(維修版)
        },
        {
            'dir': f'{WATCH_DIR}\\test',
            'token': "ZL6FZlsIN332taAC4zQBdKWukcICISoZyv6sc73AIuB" # 除錯
        }
    ]


def clearOldFiles(dir):
    print("check {0} exists: {1}".format(dir, os.path.exists(dir)))
    if not os.path.exists(dir):
        os.mkdir(dir)

    for f in os.listdir(dir):
        if not os.path.isdir(os.path.join(dir, f)):
            os.remove(os.path.join(dir, f))

class ObserverEventHandler(FileSystemEventHandler):
    def __init__(self, line_notify):
        self.observer = Observer()
        self.line_notify = line_notify

    def on_created(self, event):
        if event.is_directory:
            return
        else:
            with open(event.src_path, 'r', encoding='UTF-8') as file:
                content = file.read()
                print(content)
                self.line_notify.send(content)

def addScheduleToObserver(observer, dir, token):
    line_notify = LineNotify(token)
    handler = ObserverEventHandler(line_notify)
    observer.schedule(handler, dir, recursive=True)


if not inMac:
    clearOldFiles(WATCH_DIR)

observer = Observer()
for obj in dirs:
    clearOldFiles(obj.get('dir'))
    addScheduleToObserver(observer, obj.get('dir'), obj.get('token'))
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
