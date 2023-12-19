@echo off

pip install watchdog line_notify python-decouple pyyaml

@python lineNotify.py
@pause
