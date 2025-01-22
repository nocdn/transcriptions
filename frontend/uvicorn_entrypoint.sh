#!/bin/sh
uvicorn --host 0.0.0.0 --port 3090 --workers 3  "app:app"
