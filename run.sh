#!/bin/bash
# Speaking Practice Studio Launcher
cd "$(dirname "$0")"
exec /home/ubuntu/venvenv/bin/python3 main.py "$@"
