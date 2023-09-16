from fastapi import FastAPI, Depends, Query
from sqlite3 import Connection

from app.crud import CRUDSqlConvertTool
from app.schemas.sql_schema import SqlRequest, SqlResponse, SqlDataWithId, GetSqlResponse
from app.sql_convert_tool.main import process_query
from app.core.deps import create_table, db_connect

create_table()

app = FastAPI()


@app.get("/")
def root():
    return {"message": "sql convert tool backend started."}


@app.get("/sql", response_model=GetSqlResponse)
def get_sql(
    limit: int = 10, 
    page: int = 1,
    order_by: str = "id", 
    db: Connection = Depends(db_connect),
):
    crud = CRUDSqlConvertTool()
    offset = (page - 1) * limit
    data = crud.read_with_limit_offset_order_by(db, limit, offset, order_by)
    return {
        "data": [
            SqlDataWithId(
                id=row[0],
                sql=row[1],
                converted_sql=row[2],
                hash_map=row[3],
            )
            for row in data
        ],
        "total": len(crud.read_all(db)),
        "page": page,
        "limit": limit,
    }


@app.post("/sql", response_model=SqlResponse)
def sql(
    sql: SqlRequest, 
    db: Connection = Depends(db_connect),
):
    converted_sql, hash_map = process_query(sql.sql)
    hash_map_str = str(hash_map)

    crud = CRUDSqlConvertTool()
    crud.create(db, sql.sql, converted_sql, hash_map_str)

    return {"sql": converted_sql}

