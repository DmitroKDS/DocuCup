import re
import db.select


async def check_info(email, password):
    email = email.strip()
    password = password.strip()

    if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}\b', email):
        return "Email is incorrect"
    

    if (
        len(password)<7 
        and not any(char.isdigit() for char in password)
    ):
        return "Password is incorrect"
    

    is_user_copy = len(
        (await db.select.__init__(
            """
            SELECT id FROM users
            WHERE email = %s
            """,
            (email,)
        ))
    ) > 0

    if is_user_copy:
        return "This email is already existed"

    return email, password