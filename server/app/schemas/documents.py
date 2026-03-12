from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class UploadDocumentResponse(BaseModel):
    job_id: str
    filename: str
    size_bytes: int
    total_pages: int
    status: Literal["queued"]
    accepted_at: datetime
