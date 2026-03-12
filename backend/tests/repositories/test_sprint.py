from helpers import make_user, make_org, make_space, make_sprint
from repositories import sprint_repository
from schemas import SprintUpdate, SprintStatusCreate, SprintStatusUpdate


class TestSprintRepository:

    def test_create(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        sprint = make_sprint(session, space=space)

        assert sprint is not None
        assert sprint.spaceId == space.id

    def test_get_by_id(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        sprint = make_sprint(session, space=space)

        result = sprint_repository.get_by_id(sprint.id, session)
        assert result is not None
        assert result.id == sprint.id

    def test_get_by_id_not_found(self, session):
        result = sprint_repository.get_by_id("nonexistent-id", session)
        assert result is None

    def test_get_by_space(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        make_sprint(session, space=space, name="Sprint 1")
        make_sprint(session, space=space, name="Sprint 2")

        results = sprint_repository.get_by_space(space.id, session)
        assert len(results) == 2

    def test_get_by_space_empty(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)

        results = sprint_repository.get_by_space(space.id, session)
        assert results == []

    def test_get_active(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        sprint = make_sprint(session, space=space)

        result = sprint_repository.get_active(space.id, session)
        assert result is not None
        assert result.id == sprint.id

    def test_update_name(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        sprint = make_sprint(session, space=space)

        result = sprint_repository.update(sprint.id, SprintUpdate(name="Renamed Sprint"), session)
        assert result.name == "Renamed Sprint"

    def test_update_not_found(self, session):
        result = sprint_repository.update("nonexistent-id", SprintUpdate(name="Ghost"), session)
        assert result is None

    def test_delete(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        sprint = make_sprint(session, space=space)

        success = sprint_repository.delete(sprint.id, session)
        assert success is True
        assert sprint_repository.get_by_id(sprint.id, session) is None

    def test_delete_not_found(self, session):
        result = sprint_repository.delete("nonexistent-id", session)
        assert result is False


class TestSprintStatusRepository:

    def test_get_sprint_statuses(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)

        results = sprint_repository.get_sprint_statuses(space.id, session)
        assert len(results) > 0

    def test_create_sprint_status(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)

        status_in = SprintStatusCreate(
            name="Custom Status",
            spaceId=space.id,
            color="#ff0000",
            order=99,
        )
        result = sprint_repository.create_sprint_status(status_in, session)
        assert result is not None
        assert result.name == "Custom Status"

    def test_update_sprint_status(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        statuses = sprint_repository.get_sprint_statuses(space.id, session)
        status = statuses[0]

        result = sprint_repository.update_sprint_status(status_id=status.id, session=session, status_in=SprintStatusUpdate(name="Renamed"))
        assert result.name == "Renamed"

    def test_delete_sprint_status(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)

        status_in = SprintStatusCreate(name="Temp", spaceId=space.id, color="#000", order=99)
        status = sprint_repository.create_sprint_status(status_in, session)

        success = sprint_repository.delete_sprint_status(status.id, session)
        assert success is True