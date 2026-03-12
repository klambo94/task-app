from enums import OrgRole
from helpers import make_user, make_org
from repositories import organization_repository
from schemas import OrganizationUpdate


class TestOrganizationRepository:

    def test_create(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        assert org is not None
        assert org.name == "Test Org"
        assert org.ownerId == user.id

    def test_get_by_id(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        result = organization_repository.get_by_id(org.id, session)
        assert result is not None
        assert result.id == org.id

    def test_get_by_id_not_found(self, session):
        result = organization_repository.get_by_id("nonexistent-id", session)
        assert result is None

    def test_get_by_user(self, session):
        user = make_user(session)
        make_org(session, name="Org 1", owner_id=user.id)
        make_org(session, name="Org 2", owner_id=user.id)
        results = organization_repository.get_by_user(user.id, session)
        assert len(results) == 2

    def test_get_by_user_empty(self, session):
        user = make_user(session, email="lonely@example.com")
        results = organization_repository.get_by_user(user.id, session)
        assert results == []

    def test_update(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        updated_org = OrganizationUpdate(name="Renamed Org")
        result = organization_repository.update(org_id=org.id, org_in=updated_org, session=session)
        assert result.name == "Renamed Org"

    def test_update_not_found(self, session):
        updated_org = OrganizationUpdate(name="Ghost")
        result = organization_repository.update(org_id="nonexistent-id", org_in=updated_org, session=session)
        assert result is None

    def test_delete(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        success = organization_repository.delete(org.id, session)
        assert success is True
        assert organization_repository.get_by_id(org.id, session) is None

    def test_delete_not_found(self, session):
        result = organization_repository.delete("nonexistent-id", session)
        assert result is False


# ── OrganizationMember ────────────────────────────────────────────────────────

class TestOrganizationMemberRepository:

    def test_add_member(self, session):
        owner = make_user(session, email="owner@example.com")
        member = make_user(session, email="member@example.com")
        org = make_org(session, owner_id=owner.id)

        result = organization_repository.add_member_to_org(org.id, member.id, session=session)
        assert result is not None
        assert result.userId == member.id
        assert result.role == OrgRole.member

    def test_add_member_with_role(self, session):
        owner = make_user(session, email="owner2@example.com")
        admin = make_user(session, email="admin@example.com")
        org = make_org(session, owner_id=owner.id)

        result = organization_repository.add_member_to_org(org.id, admin.id, role=OrgRole.admin, session=session)
        assert result.role == OrgRole.admin

    def test_get_members(self, session):
        owner = make_user(session, email="owner3@example.com")
        user1 = make_user(session, email="user1@example.com")
        user2 = make_user(session, email="user2@example.com")
        org = make_org(session, owner_id=owner.id)

        organization_repository.add_member_to_org(org.id, user1.id, session=session)
        organization_repository.add_member_to_org(org.id, user2.id, session=session)

        members = organization_repository.get_members(org.id, session)
        assert len(members) == 2

    def test_update_member_role(self, session):
        owner = make_user(session, email="owner4@example.com")
        user = make_user(session, email="promote@example.com")
        org = make_org(session, owner_id=owner.id)

        organization_repository.add_member_to_org(org.id, user.id, session=session)
        result = organization_repository.update_member_role(org.id, user.id, OrgRole.admin, session)

        assert result.role == OrgRole.admin

    def test_update_member_role_not_found(self, session):
        owner = make_user(session, email="owner5@example.com")
        org = make_org(session, owner_id=owner.id)

        result = organization_repository.update_member_role(org.id, "ghost-id", OrgRole.admin, session)
        assert result is None

    def test_remove_member(self, session):
        owner = make_user(session, email="owner6@example.com")
        user = make_user(session, email="remove@example.com")
        org = make_org(session, owner_id=owner.id)

        organization_repository.add_member_to_org(org.id, user.id, session=session)
        success = organization_repository.remove_member(org.id, user.id, session)

        assert success is True
        members = organization_repository.get_members(org.id, session)
        assert all(m.userId != user.id for m in members)

    def test_remove_member_not_found(self, session):
        owner = make_user(session, email="owner7@example.com")
        org = make_org(session, owner_id=owner.id)

        result = organization_repository.remove_member(org.id, "ghost-id", session)
        assert result is False