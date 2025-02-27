from pydantic import BaseModel


class Report(BaseModel):
    id: int
    content: str