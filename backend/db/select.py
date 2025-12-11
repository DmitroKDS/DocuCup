from mysql.connector.aio import connect
import config


async def __init__(statement: str, param: tuple = None) -> list:
    async with await connect(host=config.HOST, user=config.USER, password=config.PASSWORD, database=config.DB) as db_connector:
        async with await db_connector.cursor() as db_cursor:
            await db_cursor.execute(statement, param)
            rows = await db_cursor.fetchall()

    return rows