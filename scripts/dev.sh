#! /bin/bash
if [ -d .venv ]; then
  echo "Python venv already exists"
else
  python3 -m venv .venv
fi
source "$(pwd)/.venv/bin/activate"
pip3 install -r requirements.txt
pip3 install -e .