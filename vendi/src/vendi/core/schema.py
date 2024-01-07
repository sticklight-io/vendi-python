import uuid
from datetime import datetime

from pydantic import BaseModel


class SchemaMixin(BaseModel):
    id: uuid.UUID
    """A unique identifier for the object."""
    created_at: datetime
    """The datetime timestamp the object was created."""
    updated_at: datetime
    """The datetime timestamp the object was last updated."""
    created_by: str
    """The user who created the object."""
    tenant: str
    """The tenant the object belongs to."""
