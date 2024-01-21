import logging
import smtplib

from django.conf import settings
from django.core.mail import send_mail

from blog.models import Post

logger = logging.getLogger(__name__)


class PostUserEmailSender:
    def __init__(self, post_id: int):
        self.post = Post.objects.get(pk=post_id)

    def send_email(self):
        if not self.post.user:
            logger.info(f'Post with id {self.post.id} has no user, no email will be sent.')
            return

        email = self.post.user.email

        try:
            send_mail(
                subject='Your post is published',
                message=f'Your post {self.post.title} is published.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
        except smtplib.SMTPException:
            logger.exception(f'Failed to send email to {email}. Post id: {self.post.id}')
