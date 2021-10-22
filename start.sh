#!/bin/bash
if [[ ! -e venv ]]
then
	python3 -m venv venv
fi
source ./venv/bin/activate
screen -d -m -S MerryBot python src/bot.py
