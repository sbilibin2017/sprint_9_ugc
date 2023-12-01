import motor.core as motor_core

mongo_database: motor_core.AgnosticDatabase | None = None


async def get_mongo_db() -> motor_core.AgnosticDatabase:
    if mongo_database is None:
        raise RuntimeError("client is not exists")
    return mongo_database
