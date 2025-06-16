#!/bin/bash

# Start nginx in the background
nginx &

# Start the Flask application
cd /root
python3 codesandbox_backend.py
