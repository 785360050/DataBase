from pydantic import UUID1, BaseModel


class Account_Info(BaseModel):
    uid: int
    account: str
    password: str
    name: str
    phone: int | None = None

class Request_Register(BaseModel):
    # uid: UUID1
    password: str
    name: str
    phone: int | None = None


class Request_Update(BaseModel):
    password: str | None = None
    name: str | None = None
    phone: int | None = None
