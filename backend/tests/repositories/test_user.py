from helpers import make_user
from repositories import user_repository
from schemas import UserUpdate


class TestUserRepository:

    def test_get_by_id(self, session):
        user = make_user(session)
        result = user_repository.get_by_id(user.id, session)
        assert result is not None
        assert result.id == user.id

    def test_get_by_id_not_found(self, session):
        result = user_repository.get_by_id("nonexistent-id", session)
        assert result is None

    def test_get_by_email(self, session):
        user = make_user(session, email="find@example.com")
        result = user_repository.get_by_email("find@example.com", session)
        assert result is not None
        assert result.email == "find@example.com"

    def test_get_by_email_not_found(self, session):
        result = user_repository.get_by_email("ghost@example.com", session)
        assert result is None

    def test_update_name(self, session):
        user = make_user(session)
        updated_user = UserUpdate(name="Updated Name")

        result = user_repository.update(user.id, updated_user, session=session)
        assert result.name == "Updated Name"

    def test_update_image(self, session):
        user = make_user(session)
        updated_user = UserUpdate(image="https://example.com/avatar.png")

        result = user_repository.update(user.id, user_in=updated_user, session=session)
        assert result.image == "https://example.com/avatar.png"

    def test_update_not_found(self, session):
        updated_user = UserUpdate(name="Ghost")
        result = user_repository.update("nonexistent-id", updated_user , session=session)
        assert result is None

    def test_delete(self, session):
        user = make_user(session, email="delete@example.com")
        success = user_repository.delete(user.id, session)
        assert success is True
        assert user_repository.get_by_id(user.id, session) is None

    def test_delete_not_found(self, session):
        result = user_repository.delete("nonexistent-id", session)
        assert result is False
