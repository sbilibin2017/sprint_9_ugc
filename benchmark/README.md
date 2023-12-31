# Исследование по выбору базы данных

## Цель исследования

Цель данного исследования - определить производительность баз данных в различных сценариях использования, 
включая скорость записи данных и время отклика на запросы.

## Кандидаты
 - [MongoDB](results/MongoDB/README.md)
 - [Elasticsearch](results/Elasticsearch/README.md)

## Вывод
Исходя из результатов решено использовать MongoDB с батчами по 1000 записей, так как кроме удовлетворения условию поиска 
в пределах 200мс данная БД показала ряд преимуществ:

 - Примерно в 2 раза выше скорость записи
 - Более чем в 3 раза более высокая скорость чтения записей на больших наборах данных
 - Более чем в 3 раза более высокая скорость обновления записей на больших наборах данных

## Запуск

1. Переименовать `.env.example` в `.env.example`, при необходимости наполнить своими данными;

Описание переменных:
```
CHUNK_SIZE=100               - количество записей за раз.
LIMIT_SIZE_ON_UPDATE=1000    - максимальное количество элементов, которое можно обновить за один раз.
FILLING_SIZE=250000          - размер генерации тестовых данных.

mongo_host=mongo             - хост сервера MongoDB.
mongo_user=user              - имя пользователя для подключения к MongoDB.
mongo_pass=Qwe123            - пароль пользователя для подключения к MongoDB.
mongo_port=27017             - порт, на котором работает сервер MongoDB.
mongo_db_name=bencmark_db    - имя базы данных MongoDB, с которой предполагается работа.
mongo_collection_name=events - имя коллекции в базе данных MongoDB, с которой предполагается работа.
use_mongo_index=True         - использовать ли индексирование в MongoDB.

elastic_host=http://elasticsearch - хост сервера Elasticsearch.
elastic_port=9200                 - порт, на котором работает сервер Elasticsearch.
es_index_name=events              - имя индекса в Elasticsearch, с которым предполагается работа.
```

2. Выполнить команду `docker-compose -f docker-compose.mongo.yml up -d` для Mongodb или 
`docker-compose -f docker-compose.elastic.yml up -d` для Elasticsearch; 
3. Установить зависимости из pyproject.toml;
4. Выполнить команду `python -m bin {mongodb|elastic}` для тестирования одной из баз данных. Подробнее командой
`python -m bin --help`.
