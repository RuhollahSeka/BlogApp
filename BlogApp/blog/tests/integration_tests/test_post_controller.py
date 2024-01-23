from django.test import TestCase
from model_mommy import mommy

from blog.models import Post


class PostControllerIntegrationTestCase(TestCase):
    def setUp(self) -> None:
        self.user = mommy.make('User', is_active=True, username='admin', _fill_optional=True)
        self.user.set_password('admin')
        self.user.save()

    def validate_post_response(self, post, post_data):
        self.assertEquals(post.id, post_data['id'])
        self.assertEquals(post.title, post_data['title'])
        self.assertEquals(post.content, post_data['content'])
        self.assertEquals(post.user.first_name, post_data['user']['first_name'])
        self.assertEquals(post.user.last_name, post_data['user']['last_name'])
        self.assertEquals(post.user.email, post_data['user']['email'])
        self.assertEquals(post.created_at.strftime('%Y-%m-%dT%H:%M:%S'), post_data['created_at'][:-5])
        self.assertEquals(post.updated_at.strftime('%Y-%m-%dT%H:%M:%S'), post_data['updated_at'][:-5])

    def test_post_create_retrieve_delete(self):
        response = self.client.post('/api/token/pair', {
            'username': 'admin',
            'password': 'admin',
        }, content_type='application/json')
        access_token = response.json()['access']

        response = self.client.post('/api/posts/', {
            'title': 'Test Post',
            'content': 'Test Content',
        }, content_type='application/json', HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEquals(response.status_code, 201)
        response_data = response.json()
        post = Post.objects.first()
        self.assertEquals(post.user, self.user)
        self.validate_post_response(post, response_data)

        response = self.client.get(f'/api/posts/{post.id}', HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEquals(response.status_code, 200)
        response_data = response.json()
        self.validate_post_response(post, response_data)

        response = self.client.delete(f'/api/posts/{post.id}', HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEquals(response.status_code, 204)
        self.assertEquals(Post.objects.count(), 0)

        response = self.client.get(f'/api/posts/{post.id}', HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEquals(response.status_code, 404)

    def test_post_create_list(self):
        response = self.client.post('/api/token/pair', {
            'username': 'admin',
            'password': 'admin',
        }, content_type='application/json')
        access_token = response.json()['access']

        for _ in range(20):
            response = self.client.post('/api/posts/', {
                'title': 'Test Post',
                'content': 'Test Content',
            }, content_type='application/json', HTTP_AUTHORIZATION=f'Bearer {access_token}')
            self.assertEquals(response.status_code, 201)
            response_data = response.json()
            post = Post.objects.get(id=response_data['id'])
            self.assertEquals(post.user, self.user)
            self.validate_post_response(post, response_data)

        response = self.client.get('/api/posts/?limit=10&offset=0', HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEquals(response.status_code, 200)
        response_data = response.json()
        items = response_data['items']
        self.assertEquals(len(items), 10)
        count = response_data['count']
        self.assertEquals(count, 20)
        for post_data in items:
            post = Post.objects.get(id=post_data['id'])
            self.validate_post_response(post, post_data)
