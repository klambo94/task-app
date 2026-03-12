from helpers import make_user, make_org, make_space, make_thread, auth


class TestCommentRoutes:

    def test_create_comment(self, client, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        thread = make_thread(session, space=space)
        response = client.post(
            "/api/comments",
            headers=auth(user),
            json={"content": "Hello!", "threadId": thread.id, "authorId": user.id}
        )
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["content"] == "Hello!"
        assert data["authorId"] == user.id

    def test_create_comment_forbidden(self, client, session):
        owner = make_user(session, email="owner@example.com")
        outsider = make_user(session, email="outsider@example.com")
        org = make_org(session, owner_id=owner.id)
        space = make_space(session, owner_id=owner.id, org_id=org.id)
        thread = make_thread(session, space=space)
        response = client.post(
            "/api/comments",
            headers=auth(outsider),
            json={"content": "Hacked!", "threadId": thread.id, "authorId": outsider.id}
        )
        assert response.status_code == 403

    def test_get_comments(self, client, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        thread = make_thread(session, space=space)
        client.post("/api/comments", headers=auth(user), json={"content": "First", "threadId": thread.id, "authorId": user.id})
        client.post("/api/comments", headers=auth(user), json={"content": "Second", "threadId": thread.id, "authorId": user.id})
        response = client.get(f"/api/threads/{thread.id}/comments", headers=auth(user))
        assert response.status_code == 200
        assert len(response.json()["data"]) == 2

    def test_update_comment(self, client, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        thread = make_thread(session, space=space)
        create_resp = client.post(
            "/api/comments",
            headers=auth(user),
            json={"content": "Original", "threadId": thread.id, "authorId": user.id}
        )
        comment_id = create_resp.json()["data"]["id"]
        response = client.patch(
            f"/api/comments/{comment_id}",
            headers=auth(user),
            json={"content": "Edited"}
        )
        assert response.status_code == 200
        assert response.json()["data"]["content"] == "Edited"

    def test_update_comment_forbidden(self, client, session):
        owner = make_user(session, email="owner@example.com")
        other = make_user(session, email="other@example.com")
        org = make_org(session, owner_id=owner.id)
        space = make_space(session, owner_id=owner.id, org_id=org.id)
        thread = make_thread(session, space=space)
        create_resp = client.post(
            "/api/comments",
            headers=auth(owner),
            json={"content": "Original", "threadId": thread.id, "authorId": owner.id}
        )
        comment_id = create_resp.json()["data"]["id"]
        response = client.patch(
            f"/api/comments/{comment_id}",
            headers=auth(other),
            json={"content": "Hacked"}
        )
        assert response.status_code == 403

    def test_delete_comment(self, client, session):
        user = make_user(session, email="delete@example.com")
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        thread = make_thread(session, space=space)
        create_resp = client.post(
            "/api/comments",
            headers=auth(user),
            json={"content": "Bye!", "threadId": thread.id, "authorId": user.id}
        )
        comment_id = create_resp.json()["data"]["id"]
        response = client.delete(f"/api/comments/{comment_id}", headers=auth(user))
        assert response.status_code == 200