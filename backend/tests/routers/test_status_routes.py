from helpers import make_user, make_org, make_space
from repositories import status_repository
from schemas.status_schema import StatusCreate
from enums import StatusCategory


class TestStatusRoutes:

    def test_get_status(self, client, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        response = client.get(f"/api/spaces/{space.id}/status", params={"user_id": user.id})
        assert response.status_code == 200
        assert len(response.json()["data"]) > 0  # seeded on space creation

    def test_get_status_forbidden(self, client, session):
        owner = make_user(session, email="owner@example.com")
        outsider = make_user(session, email="outsider@example.com")
        org = make_org(session, owner_id=owner.id)
        space = make_space(session, owner_id=owner.id, org_id=org.id)
        response = client.get(f"/api/spaces/{space.id}/status", params={"user_id": outsider.id})
        assert response.status_code == 403

    def test_create_status(self, client, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        response = client.post(
            f"/api/spaces/{space.id}/status",
            params={"user_id": user.id},
            json={
                "name": "Custom",
                "spaceId": space.id,
                "category": StatusCategory.STARTED.value,
                "color": "#ff0000",
                "order": 99
            }
        )
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["name"] == "Custom"
        assert data["category"] == StatusCategory.STARTED.value

    def test_create_status_forbidden_member(self, client, session):
        owner = make_user(session, email="owner@example.com")
        member = make_user(session, email="member@example.com")
        org = make_org(session, owner_id=owner.id)
        from repositories import organization_repository
        from enums import OrgRole
        organization_repository.add_member_to_org(org.id, member.id, role=OrgRole.MEMBER, session=session)
        space = make_space(session, owner_id=owner.id, org_id=org.id)
        response = client.post(
            f"/api/spaces/{space.id}/status",
            params={"user_id": member.id},
            json={"name": "Hacked", "spaceId": space.id, "category": StatusCategory.STARTED.value, "color": "#000", "order": 99}
        )
        assert response.status_code == 403

    def test_update_status(self, client, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        status = status_repository.get_by_space(space.id, session)
        status = status[0]
        response = client.patch(
            f"/api/status/{status.id}",
            params={"user_id": user.id},
            json={"name": "Renamed"}
        )
        assert response.status_code == 200
        assert response.json()["data"]["name"] == "Renamed"

    def test_update_status_not_found(self, client, session):
        user = make_user(session)
        response = client.patch(
            "/api/status/nonexistent-id",
            params={"user_id": user.id},
            json={"name": "Ghost"}
        )
        assert response.status_code == 404

    def test_reorder_status(self, client, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        status = status_repository.get_by_space(space.id, session)
        reorders = [{"id": s.id, "order": i * 10} for i, s in enumerate(status)]
        response = client.post(
            f"/api/spaces/{space.id}/status/reorder",
            params={"user_id": user.id},
            json=reorders
        )
        assert response.status_code == 200

    def test_delete_status(self, client, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        status_in = StatusCreate(
            name="Temp",
            spaceId=space.id,
            category=StatusCategory.NOT_STARTED,
            color="#000000",
            order=99
        )
        status = status_repository.create(status_in, session)
        response = client.delete(f"/api/status/{status.id}", params={"user_id": user.id})
        assert response.status_code == 200

    def test_delete_status_not_found(self, client, session):
        user = make_user(session)
        response = client.delete("/api/status/nonexistent-id", params={"user_id": user.id})
        assert response.status_code == 404