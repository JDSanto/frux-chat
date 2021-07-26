#!/bin/bash

echo 'starting server'

args=(
  -w 2
  --bind 0.0.0.0:5500 "frux_chat.main:create_app()"
)
if [[ $ENVIRONMENT == "develop" ]]; then
    args+=(--access-logfile)
    args+=(-)
fi

poetry run gunicorn "${args[@]}"
# poetry run gunicorn -w 2 --bind 0.0.0.0:5500 "frux_chat.main:create_app()" --access-logfile -
