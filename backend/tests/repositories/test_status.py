import pytest
from helpers import make_user, make_org, make_space
from repositories import status_repository
from schemas.status_schema import StatusCreate, StatusUpdate, StatusReorder
from enums import StatusCategory


class TestStatusRepository:

    def test_space_seeded_statuses(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)

        results = status_repository.get_by_space(space.id, session)
        assert len(results) > 0

    def test_get_by_id(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        statuses = status_repository.get_by_space(space.id, session)
        status = statuses[0]

        result = status_repository.get_by_id(status.id, session)
        assert result is not None
        assert result.id == status.id

    def test_get_by_id_not_found(self, session):
        result = status_repository.get_by_id("nonexistent-id", session)
        assert result is None

    def test_get_default(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)

        result = status_repository.get_default(space.id, session)
        assert result is not None
        assert result.isDefault is True

    def test_create_custom_status(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)

        status_in = StatusCreate(
            name="Custom",
            spaceId=space.id,
            category=StatusCategory.STARTED,
            color="#ff0000",
            order=99,
        )
        result = status_repository.create(status_in, session)
        assert result is not None
        assert result.name == "Custom"
        assert result.category == StatusCategory.STARTED

    def test_update(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        statuses = status_repository.get_by_space(space.id, session)
        status = statuses[0]

        result = status_repository.update(status.id, StatusUpdate(name="Renamed"), session)
        assert result.name == "Renamed"

    def test_update_not_found(self, session):
        result = status_repository.update("nonexistent-id", StatusUpdate(name="Ghost"), session)
        assert result is None

    def test_reorder(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        statuses = status_repository.get_by_space(space.id, session)

        reorders = [StatusReorder(id=s.id, order=i * 10) for i, s in enumerate(statuses)]
        result = status_repository.reorder(reorders, session)
        assert result is True

        updated = status_repository.get_by_space(space.id, session)
        assert updated[0].order == 0
        assert updated[1].order == 10

    def test_delete(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)

        status_in = StatusCreate(name="Temp", spaceId=space.id, category=StatusCategory.NOT_STARTED, color="#000", order=99)
        status = status_repository.create(status_in, session)

        success = status_repository.delete(status.id, session)
        assert success is True
        assert status_repository.get_by_id(status.id, session) is None

    def test_delete_not_found(self, session):
        result = status_repository.delete("nonexistent-id", session)
        assert result is False