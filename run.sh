#!/bin/bash
source /etc/profile
source /home/qa/python_venv_36/bin/activate
python3 /home/qa/sendEmail/flowerSendEmail.py "$1"