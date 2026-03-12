from sqlalchemy.orm import Session

from enums import SpaceVisibility, ThreadPriority
from schemas import OrganizationCreate, SpaceCreate, SprintCreate, ThreadCreate, LabelCreate
from repositories import organization_repository, space_repository, sprint_repository, thread_repository, label_repository


def make_user(session, email="test@example.com", name="Test User"):
    from models.auth_models import User
    from utils import generate_id
    from datetime import datetime

    user = User(id=generate_id(), email=email, name=name, createdAt=datetime.utcnow(), updatedAt=datetime.utcnow())
    session.add(user)
    session.flush()
    return user


def make_org(session,  owner_id:str, name="Test Org"):
    org = OrganizationCreate(name=name, ownerId=owner_id)
    return organization_repository.create(organization_in=org, session=session)

def make_space(session, owner_id: str, org_id: str, name="Test Space", visibility=SpaceVisibility.PERSONAL):
    space_in = SpaceCreate(
        name=name,
        ownerId=owner_id,
        organizationId=org_id,
        visibility=visibility,
    )
    return space_repository.create(space_in=space_in, session=session)


def make_sprint(session, space, name="Test Sprint"):
    # use the default (open) sprint status seeded for this space
    default_status = next((s for s in space.sprintStatuses if s.isDefault), space.sprintStatuses[0])
    sprint_in = SprintCreate(
        name=name,
        spaceId=space.id,
        statusId=default_status.id,
    )
    return sprint_repository.create(sprint_in=sprint_in, session=session)


def make_thread(session: Session, space, title="Test Thread", priority=ThreadPriority.NO_PRIORITY, sprint=None,
                parent_id=None,  reporter_id=None):
    default_status = next((s for s in space.statuses if s.isDefault), space.statuses[0])
    thread_in = ThreadCreate(
        title=title,
        spaceId=space.id,
        statusId=default_status.id,
        priority=priority,
        sprintId=sprint.id if sprint else None,
        parentId=parent_id,
        reporterId=reporter_id,
    )
    return thread_repository.create(thread_in=thread_in, session=session)


def make_label(session: Session, space_id: str, name="Test Label", color="#ff0000"):
    label_in = LabelCreate(name=name, spaceId=space_id, color=color)
    return label_repository.create(label_in=label_in, session=session)