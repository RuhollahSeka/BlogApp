from unittest.mock import patch

from django.conf import settings
from django.test import TestCase
from model_mommy import mommy

from blog.services import PostUserEmailSender


class PostUserEmailSenderTestCase(TestCase):
    @patch('blog.services.post_user_email_sender.send_mail')
    def test_post_without_user(self, send_mail_mock):
        post = mommy.make('Post', user=None)
        PostUserEmailSender(post.id).send_email()
        self.assertFalse(send_mail_mock.called)

    @patch('blog.services.post_user_email_sender.send_mail')
    def test_post_with_user(self, send_mail_mock):
        post = mommy.make('Post', _fill_optional=True)
        PostUserEmailSender(post.id).send_email()
        send_mail_mock.assert_called_once_with(
            subject='Your post is published',
            message=f'Your post {post.title} is published.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[post.user.email],
            fail_silently=False,
        )
