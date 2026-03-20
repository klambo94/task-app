from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.lib import CursorPage, generate_id, paginate
from app.models.user_model import User


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    # ------------------------------------------------------------------
    # Reads
    # ------------------------------------------------------------------

    def get_by_id(self, user_id: str) -> User | None:
        return (
            self.db.query(User)
            .filter(User.id == user_id, User.deletedAt.is_(None))
            .first()
        )

    def get_by_kinde_id(self, kinde_id: str) -> User | None:
        """Used by auth middleware to look up the local user from a JWT sub claim."""
        return (
            self.db.query(User)
            .filter(User.kindeId == kinde_id, User.deletedAt.is_(None))
            .first()
        )

    def get_by_email(self, email: str) -> User | None:
        return (
            self.db.query(User)
            .filter(User.email == email, User.deletedAt.is_(None))
            .first()
        )

    def list(self, cursor: str | None = None, limit: int = 20) -> CursorPage:
        query = (
            self.db.query(User)
            .filter(User.deletedAt.is_(None))
            .order_by(User.createdAt.desc(), User.id.desc())
        )
        return paginate(query, cursor, limit)

    # ------------------------------------------------------------------
    # Writes
    # ------------------------------------------------------------------

    def create(
            self,
            kinde_id: str,
            email: str,
            name: str | None,
            avatar_url: str | None,
    ) -> User:
        user = User(
            id=generate_id(),
            kindeId=kinde_id,
            email=email,
            name=name,
            avatarUrl=avatar_url,
        )
        self.db.add(user)
        self.db.flush()
        return user

    def update_or_insert_from_token(
            self,
            kinde_id: str,
            email: str,
            name: str | None,
            avatar_url: str | None,
    ) -> User:
        """
        Lazy sync from Kinde JWT claims. Creates the local user on first
        login, updates profile fields on subsequent logins if anything changed.
        """
        user = self.get_by_kinde_id(kinde_id)
        if user is None:
            return self.create(kinde_id, email, name, avatar_url)

        user.email = email
        user.name = name
        user.avatarUrl = avatar_url
        self.db.flush()
        return user

    def soft_delete(self, user: User) -> User:
        user.deletedAt = datetime.now(timezone.utc)
        self.db.flush()
        return user