from app.core.database import get_db

def create_tables():
    with get_db() as conn:
        cur=conn.cursor()
        cur.execute(
            """ Create table if not exists users (
            id SERIAL primary key,
            name varchar(125) not null,
            email varchar(125) not null,
            password text not null,
            refresh_token text,
            token_version int not null
            )"""
        )
        cur.execute(
            """
            DO $$
            BEGIN
            IF NOT EXISTS (
            SELECT 1 FROM pg_type WHERE typname = 'priority_level'
            ) THEN
            CREATE TYPE priority_level AS ENUM ('high', 'medium', 'low');
            END IF;
            END $$;
            """
        )
        cur.execute(
            """Create table if not exists Tasks(
            id SERIAL primary key,
            user_id int REFERENCES users(id),
            name varchar(250) not null,
            description text,
            is_completed boolean default false,
            priority priority_level default 'low'
            )"""
        )
        conn.commit()
        cur.close()
