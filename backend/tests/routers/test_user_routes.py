from helpers import make_user, auth


class TestUserRoutes:

    def test_get_me(self, client, session):
        user = make_user(session)
        response = client.get("/api/users/me", headers=auth(user))
        assert response.status_code == 200
        assert response.json()["data"]["id"] == user.id

    def test_get_me_unauthenticated(self, client, session):
        response = client.get("/api/users/me", headers={"Authorization": "Bearer invalidtoken"})
        assert response.status_code == 401

    def test_get_user_by_id(self, client, session):
        user = make_user(session)
        response = client.get(f"/api/users/{user.id}", headers=auth(user))
        assert response.status_code == 200
        assert response.json()["data"]["email"] == user.email

    def test_get_user_not_found(self, client, session):
        user = make_user(session)
        response = client.get("/api/users/nonexistent-id", headers=auth(user))
        assert response.status_code == 404

    def test_update_me(self, client, session):
        user = make_user(session)
        response = client.patch(
            "/api/users/me",
            headers=auth(user),
            json={"name": "Updated Name"}
        )
        assert response.status_code == 200
        assert response.json()["data"]["name"] == "Updated Name"

    def test_delete_me(self, client, session):
        user = make_user(session, email="test@example.com")
        response = client.delete("/api/users/me", headers=auth(user))
        assert response.status_code == 200
        assert response.json()["message"] == "User deleted"