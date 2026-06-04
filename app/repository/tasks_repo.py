import psycopg2
from app.core.database import get_db
from app.schema.task import TaskCreate,TaskUpdate
from psycopg2.extras import RealDictCursor

class TaskRepository():
    def create_task(self,task:TaskCreate, user_id:int):
        with get_db() as conn:
            cur=conn.cursor(cursor_factory=RealDictCursor)
            cur.execute(
                """Insert into tasks (user_id,title,description,priority) values (%s,%s,%s,%s)
                RETURNING id,user_id,title,description,is_completed,priority;""",
                (user_id,task.title,task.description,task.priority)
            )
            task=cur.fetchone()
            conn.commit()
            return task
    
    def get_tasks_by_uid(self,user_id:int):
        with get_db() as conn:
            cur=conn.cursor(cursor_factory=RealDictCursor)
            cur.execute(
                """Select * from tasks where user_id=%s;""",
                (user_id,)
            )
            tasks=cur.fetchall()
            return tasks

    def update_task(self,task:TaskUpdate,task_id:int):
        updated_task=task.dict(exclude_unset=True)
        params=[]
        values=[]
        for key,value in updated_task.items():
            params.append(f"{key}=%s")
            values.append(value)
        set_clause=" , ".join(params)
        
        with get_db() as conn:
            cur=conn.cursor(cursor_factory=RealDictCursor)
            cur.execute(
                f"""Update tasks SET {set_clause} where id=%s
                 RETURNING id,user_id,title,description,is_completed,priority;""",
                (*values,task_id,)
            )
            task=cur.fetchone()
            conn.commit()
            return task

    def delete_task(self,task_id:int):
        with get_db() as conn:
            cur=conn.cursor()
            cur.execute(
                f"""Delete from tasks where id=%s""",
                (task_id,)
            )
            conn.commit()
    
    def delete_all_tasks(self,user_id:int):
        with get_db() as conn:
            cur=conn.cursor()
            cur.execute(
                f"""Delete from tasks where user_id=%s""",
                (user_id,)
            )
            conn.commit()
        
