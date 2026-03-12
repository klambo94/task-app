from helpers import make_user, make_org, make_space, make_sprint
from schemas import SprintCreate


class TestSprintRoutes:

    def test_create_sprint(self, client, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        default_status = space.sprintStatuses[0]

        sprint = SprintCreate(name="Sprint 1", spaceId=space.id, statusId=default_status.id)
        response = client.post(
            "/api/sprints",
            params={"user_id": user.id},
            json=sprint.model_dump(mode="json")
        )
        assert response.status_code == 200
        assert response.json()["data"]["name"] == "Sprint 1"

    def test_get_sprints(self, client, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        make_sprint(session, space=space, name="Sprint 1")
        make_sprint(session, space=space, name="Sprint 2")
        response = client.get(f"/api/spaces/{space.id}/sprints", params={"user_id": user.id})
        assert response.status_code == 200
        assert len(response.json()["data"]) == 2

    def test_get_active_sprint(self, client, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        sprint = make_sprint(session, space=space)
        response = client.get(f"/api/spaces/{space.id}/sprints/active", params={"user_id": user.id})
        assert response.status_code == 200
        assert response.json()["data"]["id"] == sprint.id

    def test_get_sprint(self, client, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        sprint = make_sprint(session, space=space)
        response = client.get(f"/api/sprints/{sprint.id}", params={"user_id": user.id})
        assert response.status_code == 200
        assert response.json()["data"]["id"] == sprint.id

    def test_update_sprint(self, client, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        sprint = make_sprint(session, space=space)
        response = client.patch(
            f"/api/sprints/{sprint.id}",
            params={"user_id": user.id},
            json={"name": "Renamed Sprint"}
        )
        assert response.status_code == 200
        assert response.json()["data"]["name"] == "Renamed Sprint"

    def test_delete_sprint(self, client, session):
        user = make_user(session, email="delete@example.com")
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        sprint = make_sprint(session, space=space)
        response = client.delete(f"/api/sprints/{sprint.id}", params={"user_id": user.id})
        assert response.status_code == 200

    def test_get_sprint_statuses(self, client, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        response = client.get(f"/api/spaces/{space.id}/sprint-status", params={"user_id": user.id})
        assert response.status_code == 200
        assert len(response.json()["data"]) > 0

    def test_create_sprint_status(self, client, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        response = client.post(
            f"/api/spaces/{space.id}/sprint-status",
            params={"user_id": user.id},
            json={"name": "Custom", "color": "#ff0000", "order": 99}
        )
        assert response.status_code == 200
        assert response.json()["data"]["name"] == "Custom"