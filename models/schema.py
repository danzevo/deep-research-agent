from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone

class ResearchTask(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    query: str
    status: str = Field(default="Pending")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ResearchResult(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="researchtask.id")
    sources: str # A stringified list/JSON of the URLs we found
    report_markdown: str
    created_at: datetime = Field(default_factory=lambda:datetime.now(timezone.utc))
