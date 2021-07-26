# frux-chat

Chat service, to add push notifications and public questions to Frux.

<img src="docs/logo.png" alt="Logo" width="500px">

[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)

## What is Frux?

Frux is the newest crowdfunding app in town.

This whole project is being documented in our own [**Notion** page](https://www.notion.so/fdelmazo/frux-efab2dee3dd74d52b2a57311a1891bd4) from where you'll get the latest news, updates, documentation, and everything in between.

If you are only interested in the source code, check out the different repos!

- [frux-app-server](https://github.com/camidvorkin/frux-app-server)
- [frux-web](https://github.com/JuampiRombola/frux-web)
- [frux-mobile](https://github.com/FdelMazo/frux-mobile)
- [frux-smart-contract](https://github.com/JDSanto/frux-smart-contract)
- [frux-chat](https://github.com/JDSanto/frux-chat)

Frux is currently being developed by

- [@camidvorkin](https://www.github.com/camidvorkin)
- [@JuampiRombola](https://www.github.com/JuampiRombola)
- [@JDSanto](https://www.github.com/JDSanto)
- [@fdelmazo](https://www.github.com/FdelMazo)

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


### pre-commit hooks

You can enable linter pre-commit hooks by running:

```
poetry run pre-commit install
```

## Docs

Currently in [`/api/spec.html`](https://frux-chat.herokuapp.com/api/spec.html)
