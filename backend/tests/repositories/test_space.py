from helpers import make_user, make_org, make_space
from repositories import space_repository
from schemas import SpaceCreate, SpaceUpdate
from enums import SpaceVisibility


class TestSpaceRepository:

    def test_create(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)

        assert space is not None
        assert space.name == "Test Space"
        assert space.ownerId == user.id
        assert space.organizationId == org.id

    def test_create_seeds_statuses(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)

        assert len(space.statuses) > 0
        assert len(space.sprintStatuses) > 0

    def test_create_seeds_default_status(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)

        default_status = next((s for s in space.statuses if s.isDefault), None)
        assert default_status is not None

    def test_get_by_id(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)

        result = space_repository.get_by_id(space.id, session)
        assert result is not None
        assert result.id == space.id

    def test_get_by_id_not_found(self, session):
        result = space_repository.get_by_id("nonexistent-id", session)
        assert result is None

    def test_get_by_org(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        make_space(session, name="Space 1", owner_id=user.id, org_id=org.id)
        make_space(session, name="Space 2", owner_id=user.id, org_id=org.id)

        results = space_repository.get_by_org(org.id, session)
        assert len(results) == 2

    def test_get_by_org_empty(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)

        results = space_repository.get_by_org(org.id, session)
        assert results == []

    def test_get_by_user(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        make_space(session, name="Space 1", owner_id=user.id, org_id=org.id)
        make_space(session, name="Space 2", owner_id=user.id, org_id=org.id)

        results = space_repository.get_by_user(user.id, session)
        assert len(results) == 2

    def test_get_by_user_empty(self, session):
        user = make_user(session, email="lonely@example.com")
        results = space_repository.get_by_user(user.id, session)
        assert results == []

    def test_update_name(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)

        result = space_repository.update(space.id, SpaceUpdate(name="Renamed Space"), session)
        assert result.name == "Renamed Space"

    def test_update_visibility(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)

        result = space_repository.update(space.id, SpaceUpdate(visibility=SpaceVisibility.SHARED), session)
        assert result.visibility == SpaceVisibility.SHARED

    def test_update_not_found(self, session):
        result = space_repository.update("nonexistent-id", SpaceUpdate(name="Ghost"), session)
        assert result is None

    def test_delete(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)

        success = space_repository.delete(space.id, session)
        assert success is True
        assert space_repository.get_by_id(space.id, session) is None

    def test_delete_cascades_statuses(self, session):
        from models.status_models import Status
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        space_id = space.id

        space_repository.delete(space.id, session)

        remaining = session.query(Status).filter(Status.spaceId == space_id).all()
        assert remaining == []

    def test_delete_not_found(self, session):
        result = space_repository.delete("nonexistent-id", session)
        assert result is False