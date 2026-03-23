from fastapi import FastAPI

from app.core.config import settings
from app.routers import (
    user_router,
    org_router,
    org_invitation_router,
    invitation_router,
    org_spaces_router,
    spaces_router,
    spaces_status_router,
    status_router,
    spaces_label_router,
    label_router,
    spaces_iteration_router,
    iterations_router,
    spaces_thread_router,
    thread_router,
    thread_comment_router,
    comment_router,
    thread_attachment_router,
    comment_attachment_router,
    attachment_router,
    notification_router,
    single_notification_router,
)
app = FastAPI(
    title="Psinaptic",
    version="0.1.0",
    debug=settings.environment == "dev",
)


@app.get("/health")
def health():
    return {"status": "ok", "environment": settings.environment}

# Users
app.include_router(user_router)

# Orgs
app.include_router(org_router)
app.include_router(org_invitation_router)
app.include_router(invitation_router)

# Spaces
app.include_router(org_spaces_router)
app.include_router(spaces_router)

# Statuses
app.include_router(spaces_status_router)
app.include_router(status_router)

# Labels
app.include_router(spaces_label_router)
app.include_router(label_router)

# Iterations
app.include_router(spaces_iteration_router)
app.include_router(iterations_router)

# Threads
app.include_router(spaces_thread_router)
app.include_router(thread_router)

# Comments
app.include_router(thread_comment_router)
app.include_router(comment_router)

# Attachments
app.include_router(thread_attachment_router)
app.include_router(comment_attachment_router)
app.include_router(attachment_router)

# Notifications
app.include_router(notification_router)
app.include_router(single_notification_router)