import base64
import json
import logging

from datetime import datetime
from typing import Generic, TypeVar, Sequence, Any, Callable

from fastapi import Query
from pydantic import BaseModel

log = logging.getLogger(__name__)

T = TypeVar("T")


class CursorPage(BaseModel, Generic[T]):
    items: Sequence[T]
    nextCursor: str | None
    hasNext: bool


def encode_cursor(created_at: datetime, id: str) -> str:
    log.debug("Encoding cursor")
    payload = {
        "created_at": created_at,
        "id": id,
    }

    raw = json.dumps(payload, separators=(",", ":"))
    return base64.urlsafe_b64encode(raw.encode()).decode()

def decode_cursor(cursor: str) -> dict[str, Any]:
    try:
        raw = base64.urlsafe_b64decode(cursor.encode()).decode()
        payload = json.loads(raw)
        return {
            "createdAt": datetime.fromisoformat(payload["createdAt"]),
            "id": payload["id"],
        }
    except Exception:
        raise ValueError("Invalid or malformed cursor")

def paginate(
        query: Query,
        cursor: str | None = None,
        limit: int = 20,
        *,
        cursor_field: Callable[[Any], tuple[datetime, str]] = lambda r: (r.createdAt, r.id),
) -> CursorPage | None:
    """
        Execute a paginated query using cursor-based pagination.

        Args:
            query:        A SQLAlchemy query already filtered and ordered.
            cursor:       Encoded cursor string from a previous response, or None for first page.
            limit:        Page size (default 20).
            cursor_field: Callable that extracts (createdAt, id) from a row.
                          Override if your model uses different field names.

        Returns:
            CursorPage with items, nextCursor, and hasNext.
        """
    from sqlalchemy import and_, or_

    if cursor:
        decoded = decode_cursor(cursor)
        cursor_created_at = decoded["createdAt"]
        cursor_id = decoded["id"]

        entity = query.column_descriptions[0]["entity"]

        query = query.filter(or_(
            # Same timestamp — only grab ids that sort AFTER cursor in DESC order
            and_(entity.createdAt == cursor_created_at, entity.id < cursor_id),

            # Earlier timestamp — everything here is already past the cursor
            entity.createdAt < cursor_created_at,
            ))

        results = query.limit(limit + 1).all()

        has_next = len(results) > limit
        items = results[:limit]

        next_cursor = (
            encode_cursor(*cursor_field(items[-1]))
            if has_next and items
            else None
        )

        return CursorPage(items=items, nextCursor=next_cursor, hasNext=has_next)
    return None


