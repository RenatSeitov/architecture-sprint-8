from pydantic import BaseModel
from typing import Optional

class Report(BaseModel):
    """Информация о пользователе, извлечённая из токена."""
    preferred_username: str
    email: Optional[str] = None
    full_name: Optional[str] = None