import pytest
from helpers import make_user, make_org, make_space, make_sprint, make_thread, make_label
from repositories import thread_repository
from schemas.thread_schema import ThreadUpdate, ThreadFilter
from enums import ThreadPriority


class TestThreadRepository:

    def test_create(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        thread = make_thread(session, space=space)

        assert thread is not None
        assert thread.spaceId == space.id

    def test_get_by_id(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        thread = make_thread(session, space=space)

        result = thread_repository.get_by_id(thread.id, session)
        assert result is not None
        assert result.id == thread.id

    def test_get_by_id_not_found(self, session):
        result = thread_repository.get_by_id("nonexistent-id", session)
        assert result is None

    def test_get_by_space(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        make_thread(session, space=space, title="Thread 1")
        make_thread(session, space=space, title="Thread 2")

        results = thread_repository.get_by_space(space.id, None, session)
        assert len(results) == 2

    def test_get_by_space_filter_priority(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        make_thread(session, space=space, title="Urgent", priority=ThreadPriority.URGENT)
        make_thread(session, space=space, title="Low", priority=ThreadPriority.LOW)

        results = thread_repository.get_by_space(
            space.id, ThreadFilter(priority=ThreadPriority.URGENT), session
        )
        assert len(results) == 1
        assert results[0].title == "Urgent"

    def test_get_by_sprint(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        sprint = make_sprint(session, space=space)
        make_thread(session, space=space, sprint=sprint, title="Sprint Thread 1")
        make_thread(session, space=space, sprint=sprint, title="Sprint Thread 2")
        make_thread(session, space=space, title="Backlog Thread")  # no sprint

        results = thread_repository.get_by_sprint(sprint.id, session)
        assert len(results) == 2

    def test_get_subtasks(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        parent = make_thread(session, space=space, title="Parent")
        make_thread(session, space=space, title="Subtask 1", parent_id=parent.id)
        make_thread(session, space=space, title="Subtask 2", parent_id=parent.id)

        results = thread_repository.get_subtasks(parent.id, session)
        assert len(results) == 2

    def test_update(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        thread = make_thread(session, space=space)

        result = thread_repository.update(thread.id, ThreadUpdate(title="Updated Title"), session)
        assert result.title == "Updated Title"

    def test_update_not_found(self, session):
        result = thread_repository.update("nonexistent-id", ThreadUpdate(title="Ghost"), session)
        assert result is None

    def test_delete(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        thread = make_thread(session, space=space)

        success = thread_repository.delete(thread.id, session)
        assert success is True
        assert thread_repository.get_by_id(thread.id, session) is None

    def test_delete_not_found(self, session):
        result = thread_repository.delete("nonexistent-id", session)
        assert result is False

    def test_assign_user(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        thread = make_thread(session, space=space)

        result = thread_repository.assign_user(thread.id, user.id, session)
        assert result is not None
        assert result.userId == user.id

    def test_assign_user_idempotent(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        thread = make_thread(session, space=space)

        thread_repository.assign_user(thread.id, user.id, session)
        result = thread_repository.assign_user(thread.id, user.id, session)  # second call
        assert result is not None

        refreshed = thread_repository.get_by_id(thread.id, session)
        assert len(refreshed.assignees) == 1

    def test_unassign_user(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        thread = make_thread(session, space=space)
        thread_repository.assign_user(thread.id, user.id, session)

        success = thread_repository.unassign_user(thread.id, user.id, session)
        assert success is True

        refreshed = thread_repository.get_by_id(thread.id, session)
        assert len(refreshed.assignees) == 0

    def test_add_label(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        thread = make_thread(session, space=space)
        label = make_label(session, space_id=space.id)

        result = thread_repository.add_label(thread.id, label.id, session)
        assert result is not None

    def test_remove_label(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        thread = make_thread(session, space=space)
        label = make_label(session, space_id=space.id)
        thread_repository.add_label(thread.id, label.id, session)

        success = thread_repository.remove_label(thread.id, label.id, session)
        assert success is True

    def test_move_to_sprint(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space = make_space(session, owner_id=user.id, org_id=org.id)
        sprint = make_sprint(session, space=space)
        thread = make_thread(session, space=space)

        result = thread_repository.move_to_sprint(thread.id, sprint.id, session)
        assert result.sprintId == sprint.id

    def test_move_to_space(self, session):
        user = make_user(session)
        org = make_org(session, owner_id=user.id)
        space1 = make_space(session, owner_id=user.id, org_id=org.id, name="Space 1")
        space2 = make_space(session, owner_id=user.id, org_id=org.id, name="Space 2")
        thread = make_thread(session, space=space1)

        result = thread_repository.move_to_space(thread.id, space2.id, session)
        assert result.spaceId == space2.id
        assert result.sprintId is None