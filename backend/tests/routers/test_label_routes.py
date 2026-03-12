from helpers import make_user, make_org, make_space, make_label


class TestLabelRoutes:

    def test_create_label(self, client, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        response = client.post(
            "/api/labels",
            params={"user_id": user.id},
            json={"name": "Bug", "spaceId": space.id, "color": "#ff0000"}
        )
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["name"] == "Bug"
        assert data["spaceId"] == space.id

    def test_create_label_forbidden(self, client, session):
        owner = make_user(session, email="owner@example.com")
        outsider = make_user(session, email="outsider@example.com")
        org = make_org(session, owner_id=owner.id)
        space = make_space(session, owner_id=owner.id, org_id=org.id)
        response = client.post(
            "/api/labels",
            params={"user_id": outsider.id},
            json={"name": "Hacked", "spaceId": space.id, "color": "#000000"}
        )
        assert response.status_code == 403

    def test_get_labels(self, client, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        make_label(session, space_id=space.id, name="Label 1")
        make_label(session, space_id=space.id, name="Label 2")
        response = client.get(f"/api/spaces/{space.id}/labels", params={"user_id": user.id})
        assert response.status_code == 200
        assert len(response.json()["data"]) == 2

    def test_get_labels_empty(self, client, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        response = client.get(f"/api/spaces/{space.id}/labels", params={"user_id": user.id})
        assert response.status_code == 200
        assert response.json()["data"] == []

    def test_get_labels_forbidden(self, client, session):
        owner = make_user(session, email="owner@example.com")
        outsider = make_user(session, email="outsider@example.com")
        org = make_org(session, owner_id=owner.id)
        space = make_space(session, owner_id=owner.id, org_id=org.id)
        response = client.get(f"/api/spaces/{space.id}/labels", params={"user_id": outsider.id})
        assert response.status_code == 403

    def test_update_label(self, client, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        label = make_label(session, space_id=space.id)
        response = client.patch(
            f"/api/labels/{label.id}",
            params={"user_id": user.id},
            json={"name": "Renamed"}
        )
        assert response.status_code == 200
        assert response.json()["data"]["name"] == "Renamed"

    def test_update_label_not_found(self, client, session):
        user = make_user(session)
        response = client.patch(
            "/api/labels/nonexistent-id",
            params={"user_id": user.id},
            json={"name": "Ghost"}
        )
        assert response.status_code == 404

    def test_delete_label(self, client, session):
        user = make_user(session, email="delete@example.com")
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        label = make_label(session, space_id=space.id)
        response = client.delete(f"/api/labels/{label.id}", params={"user_id": user.id})
        assert response.status_code == 200

    def test_delete_label_not_found(self, client, session):
        user = make_user(session)
        response = client.delete("/api/labels/nonexistent-id", params={"user_id": user.id})
        assert response.status_code == 404