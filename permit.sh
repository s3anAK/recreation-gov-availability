#!/bin/bash
cd $(find ~/ -type d -name "recreation-gov-availability")
source bin/activate
python checker.py
deactivate
