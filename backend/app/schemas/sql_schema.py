from pydantic import BaseModel


class SqlRequest(BaseModel):
    sql: str


class SqlResponse(BaseModel):
    sql: str


class SqlDataWithId(BaseModel):
    id: int
    sql: str
    converted_sql: str
    hash_map: str


class GetSqlResponse(BaseModel):
    data: list[SqlDataWithId]
    total: int
    page: int
    limit: int