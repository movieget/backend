```
backend
├─ .git
├─ .github
│  └─ workflows
│     └─ CI.yml
├─ .gitignore
├─ .gitmessage.txt
├─ poetry.lock
├─ pyproject.toml
├─ README.md
├─ scripts
└─ src
   ├─ app
   │  ├─ controller
   │  │  └─ user.py
   │  └─ v1
   │     └─ user
   │        ├─ entity
   │        │  ├─ user.py
   │        │  └─ __init__.py
   │        ├─ repository
   │        │  └─ __init__.py
   │        ├─ schemas
   │        │  └─ __init__.py
   │        └─ service
   │           └─ __init__.py
   ├─ common
   │  ├─ base_models
   │  ├─ handlers
   │  │  └─ __init__.py
   │  └─ utils
   │     └─ __init__.py
   ├─ core
   │  ├─ config.py
   │  ├─ database
   │  │  ├─ connection.py
   │  │  └─ __init__.py
   │  ├─ security.py
   │  └─ __init__.py
   └─ main.py

```