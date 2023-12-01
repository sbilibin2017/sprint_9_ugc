import logging

import typer
from core.config import OlapProviders, get_olap_providers, settings
from data_management.db_research import data_filling, research_algorithm

app = typer.Typer()
logging.getLogger("elastic_transport.transport").setLevel(logging.WARNING)


@app.command(
    "research", help="This command starts research with the given OLAP provider."
)
def run_research(
    provider: OlapProviders = typer.Argument(
        ..., help="OLAP provider to use for research. "
    )
):
    providers = get_olap_providers()
    olap_provider = providers.get(provider)

    # Инициализируем базу данных и создаём бд/таблицу
    client = olap_provider()
    client.connect()

    try:
        client.create_db()
        client.create_table()

        # Очистка таблицы, если остались старые данные
        count_docs = client.get_count()
        if count_docs.execute_result > 0:
            logging.info(f"Delete old documents - {count_docs.execute_result} pieces")
            client.clear_table()

        # загружаем первоначальные данные и считаем
        load_time, count_docs = data_filling(client, settings.FILLING_SIZE)
        logging.info(
            f"Initial data loading. Time - {load_time}s. "
            f"Average recording time - {round(int(load_time)/(settings.FILLING_SIZE/settings.CHUNK_SIZE), 4)}s."
            f"The count of documents in the database - {count_docs}. "
        )
        logging.info(f"Database size - {client.get_database_size()}mb.")

        # Выполняем действия с записями после наполнения базы
        research_algorithm(client)

    finally:
        client.drop_database()
        client.disconnect()


if __name__ == "__main__":
    app()
