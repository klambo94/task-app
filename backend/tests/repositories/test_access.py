import pytest
from helpers import make_user, make_org, make_space, make_sprint, make_thread
from repositories import access_repository, organization_repository
from enums import OrgRole


class TestOrgAccess:

    def test_owner_has_owner_role(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)

        role = access_repository.get_org_role(user.id, org.id, session)
        assert role == OrgRole.OWNER

    def test_non_member_has_no_role(self, session):
        owner = make_user(session, email="owner@example.com")
        outsider = make_user(session, email="outsider@example.com")
        org = make_org(session, owner_id=owner.id)

        role = access_repository.get_org_role(outsider.id, org.id, session)
        assert role is None

    def test_is_org_member_true(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)

        assert access_repository.is_org_member(user.id, org.id, session) is True

    def test_is_org_member_false(self, session):
        owner = make_user(session, email="owner@example.com")
        outsider = make_user(session, email="outsider@example.com")
        org = make_org(session, owner_id=owner.id)

        assert access_repository.is_org_member(outsider.id, org.id, session) is False

    def test_is_org_admin_owner(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)

        assert access_repository.is_org_admin(user.id, org.id, session) is True

    def test_is_org_admin_admin_role(self, session):
        owner = make_user(session, email="owner@example.com")
        admin = make_user(session, email="admin@example.com")
        org = make_org(session, owner_id=owner.id)
        organization_repository.add_member_to_org(org.id, admin.id, role=OrgRole.ADMIN, session=session)

        assert access_repository.is_org_admin(admin.id, org.id, session) is True

    def test_is_org_admin_member_role(self, session):
        owner = make_user(session, email="owner@example.com")
        member = make_user(session, email="member@example.com")
        org = make_org(session, owner_id=owner.id)
        organization_repository.add_member_to_org(org.id, member.id, role=OrgRole.MEMBER, session=session)

        assert access_repository.is_org_admin(member.id, org.id, session) is False

    def test_is_org_owner_true(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)

        assert access_repository.is_org_owner(user.id, org.id, session) is True

    def test_is_org_owner_false_for_admin(self, session):
        owner = make_user(session, email="owner@example.com")
        admin = make_user(session, email="admin@example.com")
        org = make_org(session, owner_id=owner.id)
        organization_repository.add_member_to_org(org.id, admin.id, role=OrgRole.ADMIN, session=session)

        assert access_repository.is_org_owner(admin.id, org.id, session) is False


class TestSpaceAccess:

    def test_org_member_can_access_space(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)

        assert access_repository.can_access_space(user.id, space.id, session) is True

    def test_non_member_cannot_access_space(self, session):
        owner = make_user(session, email="owner@example.com")
        outsider = make_user(session, email="outsider@example.com")
        org = make_org(session, owner_id=owner.id)
        space = make_space(session, owner_id=owner.id, org_id=org.id)

        assert access_repository.can_access_space(outsider.id, space.id, session) is False

    def test_space_owner_can_admin_space(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)

        assert access_repository.can_admin_space(user.id, space.id, session) is True

    def test_member_cannot_admin_space(self, session):
        owner = make_user(session, email="owner@example.com")
        member = make_user(session, email="member@example.com")
        org = make_org(session, owner_id=owner.id)
        organization_repository.add_member_to_org(org.id, member.id, role=OrgRole.MEMBER, session=session)
        space = make_space(session, owner_id=owner.id, org_id=org.id)

        assert access_repository.can_admin_space(member.id, space.id, session) is False

    def test_org_admin_can_admin_space(self, session):
        owner = make_user(session, email="owner@example.com")
        admin = make_user(session, email="admin@example.com")
        org = make_org(session, owner_id=owner.id)
        organization_repository.add_member_to_org(org.id, admin.id, role=OrgRole.ADMIN, session=session)
        space = make_space(session, owner_id=owner.id, org_id=org.id)

        assert access_repository.can_admin_space(admin.id, space.id, session) is True

    def test_nonexistent_space_returns_false(self, session):
        user = make_user(session)
        assert access_repository.can_access_space(user.id, "nonexistent-id", session) is False


class TestSprintAccess:

    def test_org_member_can_access_sprint(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        sprint = make_sprint(session, space=space)

        assert access_repository.can_access_sprint(user.id, sprint.id, session) is True

    def test_outsider_cannot_access_sprint(self, session):
        owner = make_user(session, email="owner@example.com")
        outsider = make_user(session, email="outsider@example.com")
        org = make_org(session, owner_id=owner.id)
        space = make_space(session, owner_id=owner.id, org_id=org.id)
        sprint = make_sprint(session, space=space)

        assert access_repository.can_access_sprint(outsider.id, sprint.id, session) is False


class TestThreadAccess:

    def test_org_member_can_access_thread(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        thread = make_thread(session, space=space, reporter_id=user.id)

        assert access_repository.can_access_thread(user.id, thread.id, session) is True

    def test_outsider_cannot_access_thread(self, session):
        owner = make_user(session, email="owner@example.com")
        outsider = make_user(session, email="outsider@example.com")
        org = make_org(session, owner_id=owner.id)
        space = make_space(session, owner_id=owner.id, org_id=org.id)
        thread = make_thread(session, space=space, reporter_id=owner.id)

        assert access_repository.can_access_thread(outsider.id, thread.id, session) is False

    def test_reporter_can_delete_own_thread(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        thread = make_thread(session, space=space, reporter_id=user.id)

        assert access_repository.can_delete_thread(user.id, thread.id, session) is True

    def test_member_cannot_delete_others_thread(self, session):
        owner = make_user(session, email="owner@example.com")
        member = make_user(session, email="member@example.com")
        org = make_org(session, owner_id=owner.id)
        organization_repository.add_member_to_org(org.id, member.id, role=OrgRole.MEMBER, session=session)
        space = make_space(session, owner_id=owner.id, org_id=org.id)
        thread = make_thread(session, space=space, reporter_id=owner.id)

        assert access_repository.can_delete_thread(member.id, thread.id, session) is False

    def test_admin_can_delete_others_thread(self, session):
        owner = make_user(session, email="owner@example.com")
        admin = make_user(session, email="admin@example.com")
        org = make_org(session, owner_id=owner.id)
        organization_repository.add_member_to_org(org.id, admin.id, role=OrgRole.ADMIN, session=session)
        space = make_space(session, owner_id=owner.id, org_id=org.id)
        thread = make_thread(session, space=space, reporter_id=owner.id)

        assert access_repository.can_delete_thread(admin.id, thread.id, session) is True