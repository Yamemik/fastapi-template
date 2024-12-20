# FastAPI Template (backend)

![Static Badge](https://img.shields.io/badge/Yamemik-template-template)
![GitHub top language](https://img.shields.io/github/languages/top/Yamemik/fastapi-template)
![GitHub](https://img.shields.io/github/license/Yamemik/fastapi-template)
![GitHub Repo stars](https://img.shields.io/github/stars/Yamemik/fastapi-template)
![GitHub issues](https://img.shields.io/github/issues/Yamemik/fastapi-template)


## Общее описание
_____

### Стек технологий:
  - FastAPI;
  - postgreSQL;
  - docker;
  - docker-compose.


## Техническое описание
_____

### ER-Diagrams
```mermaid
erDiagram
    USER ||--|{ ORDER : makes    
    USER }|--o| ROLE: haves
    USER {
        int id PK
        date created_at
        string name                
        string email "*"
        string password "*"
        int role_id FK "*"
    }
    ORDER {
        int id PK
        string status
        int user_id FK       
    }   
    ROLE {
        int id PK
        string title "*"
        string code_name "*"
    }
```

### fastapi
```bash
# запустить сервер
$ uvicorn --factory src.main:create_app --reload
```

### команды MakeFile
```bash
# запустить контейнер с приложением
$ make app
# запустить контейнер с приложением
$ make storage
```

### docker & docker-compose
```bash
# собрать
$ docker compose -f docker_compose/app.yaml up
# ребилдинг
$ docker build --no-cache -t docker_compose-fastapi .
```

### PipENV
```bash
# install pipenv
pip install pipenv
# .venv in fold of the project
$env:PIPENV_VENV_IN_PROJECT=1
# initilization
pipenv shell
# install
pipenv install
```


## Ссылки
_____
[by Yamemik](https://github.com/Yamemik)
