from app.schema.auth import UserInCreate,UserOutput
import psycopg2
from app.core.database import get_db

class UserRepository():
    def create_user(self,userDetails:UserInCreate):
        user=userDetails
        with get_db() as conn:
            cur=conn.cursor()
            cur.execute(
                """ Insert into users (name, email, password) values (%s,%s,%s) RETURNING id, name, email""",
                (user.name,user.email,user.password)
            )
            created_user=cur.fetchone()
            conn.commit()
        return created_user
    
    def user_exist_by_email(self,email:str):
        with get_db() as conn:
            cur=conn.cursor()
            cur.execute(
                """Select 1 from users where email=%s""",
                (email,)
            )
            res=cur.fetchone()
            return res is not None
    
    def get_user_by_email(self,email:str):
        with get_db() as conn:
            cur=conn.cursor()
            cur.execute(
                """select * from users where email=%s""",
                (email,)
            )
            res=cur.fetchone()
            return res
        
    def get_user_by_id(self,id:int):
        with get_db() as conn:
            cur=conn.cursor()
            cur.execute(
                """select * from users where id=%s""",
                (id,)
            )
            res=cur.fetchone()
            return res
        
    def delete_user(self,id:int):
        with get_db() as conn:
            cur=conn.cursor()
            cur.execute(
                """Delete from users where id=%s""",
                (id,)
            )
            conn.commit()