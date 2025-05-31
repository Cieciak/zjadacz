#!/bin/bash
if [ -d .venv ]; then
  source "$(pwd)/.venv/bin/activate"
  python3 -m build
else
  echo "No python env, create it using: make init"
fi