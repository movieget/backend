```
backend
├─ .git
├─ .github
│  └─ workflows
│     └─ CI.yml
├─ .gitignore
├─ .gitmessage.txt
├─ migrations
│  └─ models
├─ poetry.lock
├─ pyproject.toml
├─ README.md
├─ scripts
│  └─ test.sh
└─ src
   ├─ app
   │  ├─ api
   │  │  ├─ root_routes.py
   │  │  ├─ v1_routes
   │  │  │  ├─ user.py
   │  │  │  └─ __init__.py
   │  │  └─ __init__.py
   │  └─ v1
   │     ├─ alert
   │     │  ├─ entity
   │     │  │  ├─ alert.py
   │     │  │  └─ __init__.py
   │     │  ├─ repository
   │     │  │  └─ __init__.py
   │     │  ├─ schemas
   │     │  │  └─ __init__.py
   │     │  └─ service
   │     │     └─ __init__.py
   │     ├─ book
   │     │  ├─ entity
   │     │  │  ├─ book.py
   │     │  │  └─ __init__.py
   │     │  ├─ repository
   │     │  │  └─ __init__.py
   │     │  ├─ schemas
   │     │  │  └─ __init__.py
   │     │  └─ service
   │     │     └─ __init__.py
   │     ├─ cinema
   │     │  ├─ entity
   │     │  │  ├─ cinema.py
   │     │  │  └─ __init__.py
   │     │  ├─ repository
   │     │  │  └─ __init__.py
   │     │  ├─ schemas
   │     │  │  └─ __init__.py
   │     │  └─ service
   │     │     └─ __init__.py
   │     ├─ favorite
   │     │  ├─ entity
   │     │  │  ├─ favorite.py
   │     │  │  └─ __init__.py
   │     │  ├─ repository
   │     │  │  └─ __init__.py
   │     │  ├─ schemas
   │     │  │  └─ __init__.py
   │     │  └─ service
   │     │     └─ __init__.py
   │     ├─ location
   │     │  ├─ entity
   │     │  │  ├─ location.py
   │     │  │  └─ __init__.py
   │     │  ├─ repository
   │     │  │  └─ __init__.py
   │     │  ├─ schemas
   │     │  │  └─ __init__.py
   │     │  └─ service
   │     │     └─ __init__.py
   │     ├─ movie
   │     │  ├─ entity
   │     │  │  ├─ movie.py
   │     │  │  └─ __init__.py
   │     │  ├─ repository
   │     │  │  └─ __init__.py
   │     │  ├─ schemas
   │     │  │  └─ __init__.py
   │     │  └─ service
   │     │     └─ __init__.py
   │     ├─ payment
   │     │  ├─ entity
   │     │  │  ├─ payment.py
   │     │  │  ├─ payment_history.py
   │     │  │  └─ __init__.py
   │     │  ├─ repository
   │     │  │  └─ __init__.py
   │     │  ├─ schemas
   │     │  │  └─ __init__.py
   │     │  └─ service
   │     │     └─ __init__.py
   │     ├─ refund
   │     │  ├─ entity
   │     │  │  ├─ refund.py
   │     │  │  └─ __init__.py
   │     │  ├─ repository
   │     │  │  └─ __init__.py
   │     │  ├─ schemas
   │     │  │  └─ __init__.py
   │     │  └─ service
   │     │     └─ __init__.py
   │     ├─ review
   │     │  ├─ entity
   │     │  │  ├─ review.py
   │     │  │  └─ __init__.py
   │     │  ├─ repository
   │     │  │  └─ __init__.py
   │     │  ├─ schemas
   │     │  │  └─ __init__.py
   │     │  └─ service
   │     │     └─ __init__.py
   │     ├─ screen
   │     │  ├─ entity
   │     │  │  ├─ screen.py
   │     │  │  ├─ screen_info.py
   │     │  │  ├─ seat.py
   │     │  │  └─ __init__.py
   │     │  ├─ repository
   │     │  │  └─ __init__.py
   │     │  ├─ schemas
   │     │  │  └─ __init__.py
   │     │  └─ service
   │     │     └─ __init__.py
   │     └─ user
   │        ├─ entity
   │        │  ├─ user.py
   │        │  └─ __init__.py
   │        ├─ repository
   │        │  └─ __init__.py
   │        ├─ schemas
   │        │  ├─ user.py
   │        │  └─ __init__.py
   │        └─ service
   │           └─ __init__.py
   ├─ common
   │  ├─ handlers
   │  │  ├─ router_handler.py
   │  │  └─ __init__.py
   │  ├─ models
   │  │  ├─ base_model.py
   │  │  ├─ consts.py
   │  │  └─ __init__.py
   │  ├─ post_construct.py
   │  └─ utils
   │     └─ __init__.py
   ├─ core
   │  ├─ configs
   │  │  └─ database_config.py
   │  ├─ database
   │  │  ├─ connection.py
   │  │  └─ __init__.py
   │  ├─ security.py
   │  └─ __init__.py
   └─ main.py

```