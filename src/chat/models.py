from pydantic import BaseModel


class MessagesBase(BaseModel):
    message: str


class Messages(MessagesBase):
    id: int
    message: str

    class Config:
        from_attributes = True
