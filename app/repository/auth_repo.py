from app.core.database import get_db

class AuthRepository():
    def update_refresh_token(self,refresh_token:str|None, user_id:int):
        with get_db() as conn:
            cur=conn.cursor()
            cur.execute(
                """Update users set refresh_token=%s where id=%s""",
                    (refresh_token,user_id,)
            )
            conn.commit()

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

