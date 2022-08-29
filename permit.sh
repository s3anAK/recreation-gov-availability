#!/bin/bash
cd $(find ~/ -type d -name "recreation-gov-availibility")
source bin/activate
python checker.py
deactivate
