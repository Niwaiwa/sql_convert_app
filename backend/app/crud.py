from sqlite3 import Connection


class CRUDSqlConvertTool():
    
    def __init__(self):
        pass

    def create(self, db: Connection, sql: str, converted_sql: str, hash_map: str):
        db.execute(
            """
            INSERT INTO sql_convert_tool (sql, converted_sql, hash_map)
            VALUES (?, ?, ?)
            """,
            (sql, converted_sql, hash_map),
        )
        db.commit()
        return sql, converted_sql, hash_map
    
    def read(self, db: Connection, id: int):
        cursor = db.execute(
            """
            SELECT id, sql, converted_sql, hash_map
            FROM sql_convert_tool
            WHERE id=?
            """,
            (id,),
        )
        return cursor.fetchone()
    
    def read_all(self, db: Connection):
        cursor = db.execute(
            """
            SELECT id, sql, converted_sql, hash_map
            FROM sql_convert_tool
            """
        )
        return cursor.fetchall()
    
    def read_with_limit_offset_order_by(self, db: Connection, limit: int, offset: int, order_by: str="id"):
        cursor = db.execute(
            f"""
            SELECT id, sql, converted_sql, hash_map
            FROM sql_convert_tool
            ORDER BY {order_by} DESC
            LIMIT ? OFFSET ?
            """,
            (limit, offset),
        )
        return cursor.fetchall()
    
    def update(self, db: Connection, id: int, sql: str, converted_sql: str, hash_map: str):
        db.execute(
            """
            UPDATE sql_convert_tool
            SET sql=?, converted_sql=?, hash_map=?
            WHERE id=?
            """,
            (sql, converted_sql, hash_map, id),
        )
        db.commit()
        return sql, converted_sql, hash_map
    
    def delete(self, db: Connection, id: int):
        db.execute(
            """
            DELETE FROM sql_convert_tool
            WHERE id=?
            """,
            (id,),
        )
        db.commit()
        return {"message": "Deleted successfully."}
    
    def delete_all(self, db: Connection):
        db.execute(
            """
            DELETE FROM sql_convert_tool
            """
        )
        db.commit()
        return {"message": "Deleted successfully."}
