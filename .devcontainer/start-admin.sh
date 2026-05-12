#!/bin/sh
set -eu

if ! pgrep -f "python3 /usr/local/bin/mrh-admin-server.py" >/dev/null; then
  nohup python3 /usr/local/bin/mrh-admin-server.py >/tmp/mrh-admin.log 2>&1 &
fi
