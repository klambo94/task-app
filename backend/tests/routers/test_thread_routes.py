from helpers import make_user, make_org, make_space, make_sprint, make_thread, make_label
from enums import ThreadPriority


class TestThreadRoutes:

    def test_create_thread(self, client, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        default_status = next(s for s in space.statuses if s.isDefault)
        response = client.post(
            "/api/threads",
            params={"user_id": user.id},
            json={"title": "My Thread", "spaceId": space.id, "statusId": default_status.id}
        )
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["title"] == "My Thread"
        assert data["reporterId"] == user.id

    def test_create_thread_forbidden(self, client, session):
        owner = make_user(session, email="owner@example.com")
        outsider = make_user(session, email="outsider@example.com")
        org = make_org(session, owner_id=owner.id)
        space = make_space(session, owner_id=owner.id, org_id=org.id)
        default_status = next(s for s in space.statuses if s.isDefault)
        response = client.post(
            "/api/threads",
            params={"user_id": outsider.id},
            json={"title": "Hacked", "spaceId": space.id, "statusId": default_status.id}
        )
        assert response.status_code == 403

    def test_get_threads(self, client, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        make_thread(session, space=space, title="Thread 1")
        make_thread(session, space=space, title="Thread 2")
        response = client.get(f"/api/spaces/{space.id}/threads", params={"user_id": user.id})
        assert response.status_code == 200
        assert len(response.json()["data"]) == 2

    def test_get_threads_filter_priority(self, client, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        make_thread(session, space=space, title="Urgent", priority=ThreadPriority.URGENT)
        make_thread(session, space=space, title="Low", priority=ThreadPriority.LOW)
        response = client.get(
            f"/api/spaces/{space.id}/threads",
            params={"user_id": user.id, "priority": ThreadPriority.URGENT.value}
        )
        assert response.status_code == 200
        assert len(response.json()["data"]) == 1
        assert response.json()["data"][0]["title"] == "Urgent"

    def test_get_thread(self, client, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        thread = make_thread(session, space=space)
        response = client.get(f"/api/threads/{thread.id}", params={"user_id": user.id})
        assert response.status_code == 200
        assert response.json()["data"]["id"] == thread.id

    def test_get_subtasks(self, client, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        parent = make_thread(session, space=space, title="Parent")
        make_thread(session, space=space, title="Sub 1", parent_id=parent.id)
        make_thread(session, space=space, title="Sub 2", parent_id=parent.id)
        response = client.get(f"/api/threads/{parent.id}/subtasks", params={"user_id": user.id})
        assert response.status_code == 200
        assert len(response.json()["data"]) == 2

    def test_update_thread(self, client, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        thread = make_thread(session, space=space)
        response = client.patch(
            f"/api/threads/{thread.id}",
            params={"user_id": user.id},
            json={"title": "Updated"}
        )
        assert response.status_code == 200
        assert response.json()["data"]["title"] == "Updated"

    def test_delete_thread(self, client, session):
        user = make_user(session, email="delete@example.com")
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        thread = make_thread(session, space=space, reporter_id=user.id)
        response = client.delete(f"/api/threads/{thread.id}", params={"user_id": user.id})
        assert response.status_code == 200

    def test_assign_user(self, client, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        thread = make_thread(session, space=space)
        response = client.post(
            f"/api/threads/{thread.id}/assign",
            params={"user_id": user.id},
            json={"userId": user.id}
        )
        assert response.status_code == 200

    def test_unassign_user(self, client, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        thread = make_thread(session, space=space)
        client.post(f"/api/threads/{thread.id}/assign", params={"user_id": user.id}, json={"userId": user.id})
        response = client.delete(f"/api/threads/{thread.id}/assign/{user.id}", params={"user_id": user.id})
        assert response.status_code == 200

    def test_add_label(self, client, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        thread = make_thread(session, space=space)
        label = make_label(session, space_id=space.id)
        response = client.post(
            f"/api/threads/{thread.id}/labels",
            params={"user_id": user.id},
            json={"labelId": label.id}
        )
        assert response.status_code == 200

    def test_remove_label(self, client, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        thread = make_thread(session, space=space)
        label = make_label(session, space_id=space.id)
        client.post(f"/api/threads/{thread.id}/labels", params={"user_id": user.id}, json={"labelId": label.id})
        response = client.delete(f"/api/threads/{thread.id}/labels/{label.id}", params={"user_id": user.id})
        assert response.status_code == 200

    def test_move_to_sprint(self, client, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        sprint = make_sprint(session, space=space)
        thread = make_thread(session, space=space)
        response = client.patch(
            f"/api/threads/{thread.id}/move-sprint",
            params={"user_id": user.id},
            json={"sprintId": sprint.id}
        )
        assert response.status_code == 200

    def test_move_to_space(self, client, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space1 = make_space(session, owner_id=user.id, org_id=org.id, name="Space 1")
        space2 = make_space(session, owner_id=user.id, org_id=org.id, name="Space 2")
        thread = make_thread(session, space=space1)
        response = client.patch(
            f"/api/threads/{thread.id}/move-space",
            params={"user_id": user.id},
            json={"spaceId": space2.id}
        )
        assert response.status_code == 200