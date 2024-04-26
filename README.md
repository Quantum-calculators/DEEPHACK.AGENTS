# DEEPHACK.AGENTS

## Развертывание и запуск приложения

Для развертывания используется Docker. Необходимо позаботиться о его установке.
Есть 2 способа развернуть приложение:
1. С помощью startapp.sh: \
 1.1. `chmod u+x startapp.sh` \
 1.2. `./startapp.sh` \
2. Выполнить напрямую команды Docker: \
 2.1. `docker network create my-network` \
 2.2. `docker container run -d --name mongodb -p 27017:27017 --network my-network mongo:6.0` \
 2.3. `docker build RestAPI/. -t restapi:0.1.0` \
 2.4. `docker container run --name fastapi-app2 -d -p 8000:8000  --network my-network restapi:0.1.0` \
 2.5. `docker build frontend/. -t front_deephack:1.0` \
 2.6. `docker container run -d -p 3000:3000 front_deephack:1.0` \

В случае успешного выполнения команд при вызове команды `docker ps` вы увидите следующий вывод:
```
CONTAINER ID   IMAGE                COMMAND                  CREATED          STATUS          PORTS                      NAMES
4d5111cf7478   front_deephack:1.0   "docker-entrypoint.s…"   1 minutes ago   Up 1 minutes   0.0.0.0:3000->3000/tcp     elegant_wescoff
94f6871d8712   restapi:0.1.0        "uvicorn main:app --…"   1 minutes ago   Up 1 minutes   0.0.0.0:8000->8000/tcp     fastapi-app2
8a874b321004   mongo:6.0            "docker-entrypoint.s…"   1 minutes ago   Up 1 minutes   0.0.0.0:27017->27017/tcp   mongodb
```

Доступ к приложению осуществляется по адресу http://localhost:3000

## Описание решения

В науке часто возникает потребность строить различные графики для визуализации процессов или проверки статистических гипотез.
Основной идеей нашего решения является предоставление возможности GigaChat строить графики для решения прикладных и научных задач.

Типы реализованых графиков по запросам:
- График функции.
- График плотности распределения.
- График по точкам.

Построение графика в GigaChat реализовано следующим образом:
1. Определяется, требуется ли пользователю построить график.
2. Определение типа графика.
3. Определение, имеется ли данный тип графика в пресетах.
4. Определение точек графика.

## Структура приложения

Приложение является клиент-серверным. Технологический стэк:
- FastAPI
- MongoDB
- React
- MiraJS (mock)
- Docker
- GigaChat

