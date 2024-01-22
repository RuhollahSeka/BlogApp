from celery import shared_task

from BlogApp import constants
from blog.services import PostUserEmailSender


@shared_task(
    name=constants.SEND_BLOG_EMAIL_TASK,
)
def send_blog_email_task(post_id: int):
    PostUserEmailSender(post_id=post_id).send_email()
