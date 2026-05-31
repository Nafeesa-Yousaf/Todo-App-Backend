from app.core.database import get_db

class AuthRepository():
    def get_refresh_token(self,user_id:int):
        with get_db() as conn:
            cur=conn.cursor()
            cur.execute(
                """Select refresh_token from users where id=%s""",
                (user_id,)
            )
            res=cur.fetchone()
            if res:
                return res[0]
            else:
                return None

    def update_auth_fields(self, user_id: int, **fields):
        if not fields:
            return
        set_parts = []
        values = []
        for key, value in fields.items():
            if isinstance(value, str) and value.startswith("+"):
                set_parts.append(f"{key} = {key} + %s")
                values.append(int(value[1:]))
            else:
                set_parts.append(f"{key} = %s")
                values.append(value)
        set_clause = ", ".join(set_parts)
        values.append(user_id)
        query = f"UPDATE users SET {set_clause} WHERE id=%s"
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute(query, values)
            conn.commit()

    def get_token_version(self,user_id:int):
        with get_db() as conn:
            cur=conn.cursor()
            cur.execute(
                """Select token_version from users where id=%s""",
                (user_id,)
            )
            res=cur.fetchone()
            if res:
                return res[0]
            else:
                return None
