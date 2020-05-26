#!/bin/bash

mkdir gb_chat_venv && cd gb_chat_venv

python3 -m venv env

source env/bin/activate

cd ..

pip3  -r requirements.txt