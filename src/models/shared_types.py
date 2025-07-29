from typing import Annotated, Optional
from datetime import datetime, timezone
from sqlalchemy import TIMESTAMP, DateTime, text
from sqlalchemy.orm import mapped_column

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(
    DateTime(timezone=True),
    server_default=text("TIMEZONE('utc', now())"),
    nullable=False
)]
updated_at = Annotated[datetime, mapped_column(
    DateTime(timezone=True), 
    server_default=text("TIMEZONE('utc', now())"),
    onupdate=datetime.now(timezone.utc),
    nullable=False
)]
correct_datetime = Annotated[Optional[datetime], mapped_column(
    TIMESTAMP(timezone=True), 
    nullable=True
)]
