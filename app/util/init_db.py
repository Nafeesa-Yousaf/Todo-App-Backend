from app.core.database import get_db

def create_tables():
    with get_db() as conn:
        cur=conn.cursor()
        cur.execute(
            """ Create table if not exists Users (
            id SERIAL primary key,
            name varchar(125) not null,
            email varchar(125) not null,
            password text not null
            )"""
        )
        conn.commit()
        cur.close()
