# frux-chat

[Link to heroku](https://frux-chat.herokuapp.com/api/spec.html)

## Develop environment

### With docker-compose

Just run `docker-compose up --build` to have the server running with MongoDB!

### Running locally without docker

1. Install `poetry`
2. Run `poetry install`
3. Setup the following env variables:
```
DATABASE_URL=<mongo-uri>
DATABASE_NAME=frux_chat
```
4. Run `FLASK_APP=$(pwd)/frux_chat/main.py poetry run flask run`


## Docs

Currently in [`/api/spec.html`](https://frux-chat.herokuapp.com/api/spec.html)