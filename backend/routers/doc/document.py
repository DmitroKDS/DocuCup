import uuid

import db.select


async def check_info(id, title, user_id):
    if len(title) < 5:
        return "Invalid title"
    
    try:
        uuid.UUID(id)
    except ValueError:
        return "Invalid id"
    

    is_id_copy = len(
        (await db.select.__init__(
            """
            SELECT id FROM documents
            WHERE id = %s
            """,
            (id,)
        ))
    ) > 0

    if is_id_copy:
        return "This id is already existed"
    

    is_id_copy = len(
        (await db.select.__init__(
            """
            SELECT id FROM users
            WHERE id = %s
            """,
            (user_id,)
        ))
    ) == 0

    if is_id_copy:
        return "User id is not existed"

    return True