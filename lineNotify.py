# coding=utf-8
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from line_notify import LineNotify
from decouple import config
import yaml
import sys

is_windows = hasattr(sys, 'getwindowsversion')
is_test = config('IS_TEST', default='False') == 'True'

SLASH =  '\\' if is_windows else '/'

def getDir(ary):
    return SLASH.join(ary)

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
            with open(event.src_path, 'r', encoding='Big5') as file:
                content = file.read()
                print(content)
                self.line_notify.send(content)

class XqLineNotify():
    def __init__(self):
        self.__load_setting()
        self.__load_tokens()
        self.observer = Observer()

    def run(self):
        self.__add_dirs_to_observer()
        self.observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()

        self.observer.join()

    def __load_setting(self):
        with open('settings.yml', 'r', encoding="utf-8") as stream:
            self.settings = yaml.load(stream, Loader=yaml.CLoader)

    def __load_tokens(self):
        with open('tokens.yml', 'r', encoding="utf-8") as stream:
            self.tokens = yaml.load(stream, Loader=yaml.CLoader)

    def generate_dirs(self, setting):
        path = self.settings['base_dir'].copy()
        path.append(setting.get('dir'))
        return {
            'dir': getDir(path),
            'token': setting.get('token')
        }

    def __add_dirs_to_observer(self):
        if is_windows == False or is_test == True:
            dir = ''
            clearOldFiles(dir)
            self.__addScheduleToObserver(dir, config('TOKEN', default=''))
        else:
            for obj in list(map(self.generate_dirs, self.tokens)):
                clearOldFiles(obj.get('dir'))
                self.__addScheduleToObserver(obj.get('dir'), obj.get('token'))

    def __addScheduleToObserver(self, dir, token):
        line_notify = LineNotify(token)
        handler = ObserverEventHandler(line_notify)
        self.observer.schedule(handler, dir, recursive=True)

XqLineNotify().run()
