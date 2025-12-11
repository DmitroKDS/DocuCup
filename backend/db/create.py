from mysql.connector.aio import connect
import config

async def __init__() -> None:
    async with await connect(host=config.HOST, user=config.USER, password=config.PASSWORD, database=config.DB) as db_connector:
        async with await db_connector.cursor() as db_cursor:
            await db_cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS users (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    email VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    credits INTEGER(255) NOT NULL,
                    created_at DATETIME NOT NULL
                );
                '''
            )

            await db_cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS documents (
                    id VARCHAR(255) PRIMARY KEY,
                    user_id INT,
                    title VARCHAR(255) NOT NULL,
                    created_at DATETIME NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                );
                '''
            )

        await db_connector.commit()