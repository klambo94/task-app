from helpers import make_user, make_org, auth
from repositories import organization_repository
from enums import OrgRole


class TestOrgRoutes:

    def test_create_org(self, client, session):
        user = make_user(session)
        response = client.post(
            "/api/orgs/",
            headers=auth(user), params={"org_name": "My Org"},
        )
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["name"] == "My Org"
        assert data["ownerId"] == user.id


    def test_get_orgs(self, client, session):
        user = make_user(session)
        make_org(session, owner_id=user.id, name="Org 1")
        make_org(session, owner_id=user.id, name="Org 2")
        response = client.get("/api/orgs/", headers=auth(user))
        assert response.status_code == 200
        assert len(response.json()["data"]) == 2

    def test_get_org(self, client, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        response = client.get(f"/api/orgs/{org.id}", headers=auth(user))
        assert response.status_code == 200
        assert response.json()["data"]["id"] == org.id

    def test_get_org_forbidden(self, client, session):
        owner = make_user(session, email="owner@example.com")
        outsider = make_user(session, email="outsider@example.com")
        org = make_org(session, owner_id=owner.id)
        response = client.get(f"/api/orgs/{org.id}", headers=auth(outsider))
        assert response.status_code == 403

    def test_get_org_not_found(self, client, session):
        user = make_user(session)
        response = client.get("/api/orgs/nonexistent-id", headers=auth(user))
        assert response.status_code == 403  # not member → 403 before 404

    def test_update_org(self, client, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        response = client.patch(
            f"/api/orgs/{org.id}",
            headers=auth(user),
            json={"name": "Renamed Org"}
        )
        assert response.status_code == 200
        assert response.json()["data"]["name"] == "Renamed Org"

    def test_update_org_forbidden_member(self, client, session):
        owner = make_user(session, email="owner@example.com")
        member = make_user(session, email="member@example.com")
        org = make_org(session, owner_id=owner.id)
        organization_repository.add_member_to_org(org.id, member.id, role=OrgRole.MEMBER, session=session)
        response = client.patch(
            f"/api/orgs/{org.id}",
            headers=auth(member),
            json={"name": "Hacked"}
        )
        assert response.status_code == 403

    def test_delete_org(self, client, session):
        user = make_user(session, email="delete@example.com")
        org = make_org(session, owner_id=user.id)
        response = client.delete(f"/api/orgs/{org.id}", headers=auth(user))
        assert response.status_code == 200

    def test_delete_org_forbidden_admin(self, client, session):
        owner = make_user(session, email="owner@example.com")
        admin = make_user(session, email="admin@example.com")
        org = make_org(session, owner_id=owner.id)
        organization_repository.add_member_to_org(org.id, admin.id, role=OrgRole.ADMIN, session=session)
        response = client.delete(f"/api/orgs/{org.id}", headers=auth(admin))
        assert response.status_code == 403


class TestOrgMemberRoutes:

    def test_get_members(self, client, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        response = client.get(f"/api/orgs/{org.id}/members", headers=auth(user))
        assert response.status_code == 200
        assert len(response.json()["data"]) == 1  # owner auto-added

    def test_add_member(self, client, session):
        owner = make_user(session, email="owner@example.com")
        new_member = make_user(session, email="new@example.com")
        org = make_org(session, owner_id=owner.id)
        response = client.post(
            f"/api/orgs/{org.id}/members",
            headers=auth(owner),
            json={"userId": new_member.id, "role": OrgRole.MEMBER.value}
        )
        assert response.status_code == 200
        assert response.json()["data"]["userId"] == new_member.id

    def test_add_member_forbidden(self, client, session):
        owner = make_user(session, email="owner@example.com")
        member = make_user(session, email="member@example.com")
        new_user = make_user(session, email="new@example.com")
        org = make_org(session, owner_id=owner.id)
        organization_repository.add_member_to_org(org.id, member.id, role=OrgRole.MEMBER, session=session)
        response = client.post(
            f"/api/orgs/{org.id}/members",
            headers=auth(member),
            json={"userId": new_user.id, "role": OrgRole.MEMBER.value}
        )
        assert response.status_code == 403

    def test_update_member_role(self, client, session):
        owner = make_user(session, email="owner@example.com")
        member = make_user(session, email="member@example.com")
        org = make_org(session, owner_id=owner.id)
        organization_repository.add_member_to_org(org.id, member.id, role=OrgRole.MEMBER, session=session)
        response = client.patch(
            f"/api/orgs/{org.id}/members/{member.id}",
            headers=auth(owner),
            json={"role": OrgRole.ADMIN.value}
        )
        assert response.status_code == 200
        assert response.json()["data"]["role"] == OrgRole.ADMIN.value

    def test_remove_member(self, client, session):
        owner = make_user(session, email="owner@example.com")
        member = make_user(session, email="member@example.com")
        org = make_org(session, owner_id=owner.id)
        organization_repository.add_member_to_org(org.id, member.id, role=OrgRole.MEMBER, session=session)
        response = client.delete(
            f"/api/orgs/{org.id}/members/{member.id}",
            headers=auth(owner)
        )
        assert response.status_code == 200