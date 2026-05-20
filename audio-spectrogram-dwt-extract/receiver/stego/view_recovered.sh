#!/bin/bash
set -e
cd "$(dirname "$0")"
if [ ! -s recovered_secret.png ]; then
    echo "recovered_secret.png chua ton tai."
    exit 1
fi
printf 'opened\n' > .recovered_image_viewed
python3 refresh_status.py >/dev/null 2>&1 || true
exec feh recovered_secret.png
