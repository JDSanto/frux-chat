
poetry run gunicorn -w 4 --log-level=debug --bind 0.0.0.0:$PORT "frux_chat.main:create_app()"
