# FastAPI Hello — Docker Compose (FastAPI + Postgres + Redis)

Проект для курса **«Быстрый старт в FastAPI Python»**: [https://stepik.org/course/179694/](https://stepik.org/course/179694/)

## Стек

* **FastAPI**
* **PostgreSQL** и **Redis** (через Docker Compose)
* **Gunicorn** + `uvicorn.workers.UvicornWorker`

## Структура проекта

```
fastapi-hello/
├─ app/
│  └─ main.py
├─ Dockerfile
├─ requirements.txt
├─ compose.yaml
├─ compose.override.yaml
├─ compose.mirror.yaml       # опционально: зеркала образов
├─ compose.build-host.yaml   # опционально: сборка через сеть хоста
├─ Makefile
├─ .env.example
├─ .dockerignore
└─ .gitignore
```

## Быстрый старт

```bash
git clone https://github.com/Cheater121/fastapi-hello.git
cd fastapi-hello

cp .env.example .env
make upb

curl -fsS http://127.0.0.1:8000/health
```

Остановить:

```bash
make down
```

## Команды Make

```bash
make up                 # docker compose up -d
make upb                # docker compose up -d --build
make down               # остановка и удаление контейнеров/сети
make ps                 # статусы
make logs               # логи всех сервисов
make logs-f             # логи в режиме tail -f
make bash               # shell внутри контейнера app
make db-psql            # psql в контейнере БД
make redis-cli          # redis-cli в контейнере Redis
make rebuild            # пересборка образа app без кэша

# варианты с оверлеями
make up-mirror          # запуск с compose.mirror.yaml
make upb-mirror         # сборка и запуск с зеркалом
make upb-host           # сборка через сеть хоста (фикс DNS на build-этапе)
make upb-host-mirror    # сборка через сеть хоста + зеркала
make pull               # docker compose pull
make pull-mirror        # pull через compose.mirror.yaml
make dns-test           # проверка DNS внутри контейнера
```

## Overlay-файлы

* `compose.override.yaml` — локальная разработка (открывает порт 8000 наружу).
* `compose.mirror.yaml` — запуск/сборка с зеркальными образами (обход rate-limit).
* `compose.build-host.yaml` — сборка через сеть хоста (устойчивее `apt-get` на build-этапе).

> За подробной инструкцией по запуску на сервере и разбором нюансов — в курсе: [https://stepik.org/course/179694/](https://stepik.org/course/179694/)
