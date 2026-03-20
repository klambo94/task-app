from datetime import datetime, UTC

from sqlalchemy import Column, DateTime


class TimestampMixin:
    """Adds createdAt, updatedAt, and deletedAt to every model."""

    createdAt = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.now(UTC),
        doc="UTC timestamp of record creation.",
    )
    updatedAt = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.now(UTC),
        onupdate=datetime.now(UTC),
        doc="UTC timestamp of last update; auto-refreshed on every write.",
    )
    deletedAt = Column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
        doc="UTC timestamp of soft deletion. NULL means the record is active.",
    )