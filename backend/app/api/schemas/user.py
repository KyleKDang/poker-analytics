from sqlmodel import SQLModel


class UserCreate(SQLModel):
    username: str
    email: str
    password: str

    class Config:
        orm_mode = True


class UserRead(SQLModel):
    id: int
    username: str
    created_at: str
    is_active: bool

    class Config:
        orm_mode = True
