from app.routers.users_router import router as user_router
from app.routers.orgs_router import router as org_router
from app.routers.spaces_router import org_spaces_router, spaces_router
from app.routers.statuses_router import spaces_status_router, status_router
from app.routers.labels_router import spaces_label_router, label_router
from app.routers.iterations_router import spaces_iteration_router, iterations_router
from app.routers.threads_router import spaces_thread_router, thread_router
from app.routers.comments_router import thread_comment_router, comment_router
from app.routers.attachments_router import thread_attachment_router, comment_attachment_router, attachment_router
from app.routers.invitation_router import org_invitation_router, invitation_router
from app.routers.notification_router import notification_router, single_notification_router