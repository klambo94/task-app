import json

from helpers import make_user, make_org, make_space
from schemas import SpaceCreate


class TestSpaceRoutes:

    def test_create_space(self, client, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = SpaceCreate(name="My Space", ownerId=user.id, organizationId=org.id)
        response = client.post("/api/spaces/", params={"user_id": user.id}, json=space.model_dump(mode="json"))
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["name"] == "My Space"
        assert data["ownerId"] == user.id

    def test_create_space_forbidden(self, client, session):
        owner = make_user(session, email="owner@example.com")
        outsider = make_user(session, email="outsider@example.com")
        org = make_org(session, owner_id=owner.id)
        space = SpaceCreate(name="Hacked Space", ownerId=owner.id,
                            organizationId=org.id)  # ✅ SpaceCreate, not make_space
        response = client.post("/api/spaces/", params={"user_id": outsider.id}, json=space.model_dump(mode="json"))
        assert response.status_code == 403

    def test_get_spaces_by_org(self, client, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)

        space1 = SpaceCreate(name="My Space 1", ownerId=user.id, organizationId=org.id)
        space2 = SpaceCreate(name="Space 2", ownerId=user.id, organizationId=org.id)

        response1 = client.post("/api/spaces/", params={"user_id": user.id}, json=space1.model_dump(mode="json"))
        response2 = client.post("/api/spaces/", params={"user_id": user.id}, json=space2.model_dump(mode="json"))

        assert response1.status_code == 200
        assert response2.status_code == 200

        allSpaceResp = client.get("/api/spaces/", params={"user_id": user.id, "org_id": org.id})

        assert allSpaceResp.status_code == 200
        assert len(allSpaceResp.json()["data"]) == 2

    def test_get_spaces_by_user(self, client, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)

        space1 = SpaceCreate(name="My Space 1", ownerId=user.id, organizationId=org.id)
        space2 = SpaceCreate(name="Space 2", ownerId=user.id, organizationId=org.id)

        response1 = client.post("/api/spaces/", params={"user_id": user.id}, json=space1.model_dump(mode="json"))
        response2 = client.post("/api/spaces/", params={"user_id": user.id}, json=space2.model_dump(mode="json"))

        assert response1.status_code == 200
        assert response2.status_code == 200

        allSpaceResp = client.get("/api/spaces/", params={"user_id": user.id})

        assert allSpaceResp.status_code == 200
        assert len(allSpaceResp.json()["data"]) == 2

    def test_get_space(self, client, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        response = client.get(f"/api/spaces/{space.id}", params={"user_id": user.id})
        assert response.status_code == 200
        assert response.json()["data"]["id"] == space.id

    def test_get_space_forbidden(self, client, session):
        owner = make_user(session, email="owner@example.com")
        outsider = make_user(session, email="outsider@example.com")
        org = make_org(session, owner_id=owner.id)
        space = make_space(session, owner_id=owner.id, org_id=org.id)
        response = client.get(f"/api/spaces/{space.id}", params={"user_id": outsider.id})
        assert response.status_code == 403

    def test_update_space(self, client, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        response = client.patch(
            f"/api/spaces/{space.id}",
            params={"user_id": user.id},
            json={"name": "Renamed Space"}
        )
        assert response.status_code == 200
        assert response.json()["data"]["name"] == "Renamed Space"

    def test_delete_space(self, client, session):
        user = make_user(session, email="delete@example.com")
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        response = client.delete(f"/api/spaces/{space.id}", params={"user_id": user.id})
        assert response.status_code == 200