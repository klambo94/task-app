import pytest
from helpers import make_user, make_org, make_space, make_label
from repositories import label_repository
from schemas.label_schema import LabelCreate, LabelUpdate


class TestLabelRepository:

    def test_create(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        label = make_label(session, space_id=space.id)

        assert label is not None
        assert label.name == "Test Label"
        assert label.spaceId == space.id

    def test_get_by_id(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        label = make_label(session, space_id=space.id)

        result = label_repository.get_by_id(label.id, session)
        assert result is not None
        assert result.id == label.id

    def test_get_by_id_not_found(self, session):
        result = label_repository.get_by_id("nonexistent-id", session)
        assert result is None

    def test_get_by_space(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        make_label(session, space_id=space.id, name="Label 1")
        make_label(session, space_id=space.id, name="Label 2")

        results = label_repository.get_by_space(space.id, session)
        assert len(results) == 2

    def test_get_by_space_empty(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)

        results = label_repository.get_by_space(space.id, session)
        assert results == []

    def test_update(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        label = make_label(session, space_id=space.id)

        result = label_repository.update(label.id, LabelUpdate(name="Renamed"), session)
        assert result.name == "Renamed"

    def test_update_color(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        label = make_label(session, space_id=space.id)

        result = label_repository.update(label.id, LabelUpdate(color="#00ff00"), session)
        assert result.color == "#00ff00"

    def test_update_not_found(self, session):
        result = label_repository.update("nonexistent-id", LabelUpdate(name="Ghost"), session)
        assert result is None

    def test_delete(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        label = make_label(session, space_id=space.id)

        success = label_repository.delete(label.id, session)
        assert success is True
        assert label_repository.get_by_id(label.id, session) is None

    def test_delete_not_found(self, session):
        result = label_repository.delete("nonexistent-id", session)
        assert result is False