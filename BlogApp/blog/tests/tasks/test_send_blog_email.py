from unittest.mock import patch

from django.test import TestCase
from model_mommy import mommy

from blog.tasks import send_blog_email_task


class SendBlogEmailTaskTestCase(TestCase):
    @patch('blog.services.PostUserEmailSender.send_email')
    def test_send_blog_email(self, email_sender_mock):
        post = mommy.make('Post')
        send_blog_email_task(post.id)
        email_sender_mock.assert_called_once()
