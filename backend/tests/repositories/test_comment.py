import pytest
from helpers import make_user, make_org, make_space, make_thread
from repositories import comment_repository
from schemas.comment_schema import CommentCreate, CommentUpdate


class TestCommentRepository:

    def test_create(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        thread = make_thread(session, space=space)

        comment_in = CommentCreate(content="Hello!", threadId=thread.id, authorId=user.id)
        comment = comment_repository.create(comment_in, session)

        assert comment is not None
        assert comment.content == "Hello!"
        assert comment.threadId == thread.id
        assert comment.authorId == user.id

    def test_get_by_id(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        thread = make_thread(session, space=space)

        comment_in = CommentCreate(content="Hello!", threadId=thread.id, authorId=user.id)
        comment = comment_repository.create(comment_in, session)

        result = comment_repository.get_by_id(comment.id, session)
        assert result is not None
        assert result.id == comment.id

    def test_get_by_id_not_found(self, session):
        result = comment_repository.get_by_id("nonexistent-id", session)
        assert result is None

    def test_get_by_thread(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        thread = make_thread(session, space=space)

        comment_repository.create(CommentCreate(content="First", threadId=thread.id, authorId=user.id), session)
        comment_repository.create(CommentCreate(content="Second", threadId=thread.id, authorId=user.id), session)

        results = comment_repository.get_by_thread(thread.id, session)
        assert len(results) == 2

    def test_get_by_thread_empty(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        thread = make_thread(session, space=space)

        results = comment_repository.get_by_thread(thread.id, session)
        assert results == []

    def test_update(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        thread = make_thread(session, space=space)

        comment = comment_repository.create(CommentCreate(content="Original", threadId=thread.id, authorId=user.id), session)
        result = comment_repository.update(comment.id, CommentUpdate(content="Edited"), session)
        assert result.content == "Edited"

    def test_update_not_found(self, session):
        result = comment_repository.update("nonexistent-id", CommentUpdate(content="Ghost"), session)
        assert result is None

    def test_delete(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        thread = make_thread(session, space=space)

        comment = comment_repository.create(CommentCreate(content="Bye!", threadId=thread.id, authorId=user.id), session)
        success = comment_repository.delete(comment.id, session)
        assert success is True
        assert comment_repository.get_by_id(comment.id, session) is None

    def test_delete_not_found(self, session):
        result = comment_repository.delete("nonexistent-id", session)
        assert result is False