## Запуск проекта

1. Файл `.env.example` скопировать и переименовать в `.env`:
    ```bash
    cp .env.example .env
    ```

2. Запустить сервисы:
    ```bash
    make
    ```
3. Выполнить тесты:
    ```bash
    cd tests
    cp .env.example .env
    pytest
    cd ..
    ```
4. Для остановки используйте:
    ```bash
    make stop
    ```

### Документация API
Открыть в браузере [адрес](http://localhost/api/openapi) API.
