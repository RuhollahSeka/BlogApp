from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from model_mommy import mommy

from blog.models import Post


def mock_jwt_auth(request):
    user = User.objects.first()
    request.user = user
    return user


class PostControllerTestCase(TestCase):
    def setUp(self):
        self.user = mommy.make('User', is_active=True, _fill_optional=True)

    def validate_post_response(self, post, post_data):
        self.assertEquals(post.id, post_data['id'])
        self.assertEquals(post.title, post_data['title'])
        self.assertEquals(post.content, post_data['content'])
        self.assertEquals(post.user.first_name, post_data['user']['first_name'])
        self.assertEquals(post.user.last_name, post_data['user']['last_name'])
        self.assertEquals(post.user.email, post_data['user']['email'])
        self.assertEquals(post.created_at.strftime('%Y-%m-%dT%H:%M:%S'), post_data['created_at'][:-5])
        self.assertEquals(post.updated_at.strftime('%Y-%m-%dT%H:%M:%S'), post_data['updated_at'][:-5])

    def test_post_create_unauthorized(self):
        response = self.client.post('/api/posts/', {
            'title': 'Test Post',
            'content': 'Test Content',
        }, content_type='application/json')
        self.assertEquals(response.status_code, 401)

    @patch('blog.api.controllers.post.JWTAuth.__call__')
    def test_post_create(self, authenticate_mock):
        authenticate_mock.side_effect = mock_jwt_auth
        response = self.client.post('/api/posts/', {
            'title': 'Test Post',
            'content': 'Test Content',
        }, content_type='application/json')
        self.assertEquals(response.status_code, 201)
        response_data = response.json()
        post = Post.objects.first()
        self.assertEquals(post.user, self.user)
        self.validate_post_response(post, response_data)

    @patch('blog.api.controllers.post.JWTAuth.__call__')
    def test_post_update(self, authenticate_mock):
        authenticate_mock.side_effect = mock_jwt_auth
        post = mommy.make('Post', _fill_optional=True)
        response = self.client.put(f'/api/posts/{post.id}', {
            'title': 'Test Post',
            'content': 'Test Content',
        }, content_type='application/json')
        self.assertEquals(response.status_code, 200)
        response_data = response.json()
        post.refresh_from_db()
        self.assertEquals(post.title, 'Test Post')
        self.assertEquals(post.content, 'Test Content')
        self.validate_post_response(post, response_data)

    @patch('blog.api.controllers.post.JWTAuth.__call__')
    def test_post_list(self, authenticate_mock):
        authenticate_mock.side_effect = mock_jwt_auth
        mommy.make('Post', _quantity=20, _fill_optional=True)
        response = self.client.get('/api/posts/?limit=10&offset=0', content_type='application/json')
        self.assertEquals(response.status_code, 200)
        response_data = response.json()
        items = response_data['items']
        self.assertEquals(len(items), 10)
        count = response_data['count']
        self.assertEquals(count, 20)
        for post_data in items:
            post = Post.objects.get(id=post_data['id'])
            self.validate_post_response(post, post_data)

    @patch('blog.api.controllers.post.JWTAuth.__call__')
    def test_post_retrieve(self, authenticate_mock):
        authenticate_mock.side_effect = mock_jwt_auth
        post = mommy.make('Post', _fill_optional=True)
        response = self.client.get(f'/api/posts/{post.id}', content_type='application/json')
        self.assertEquals(response.status_code, 200)
        response_data = response.json()
        self.validate_post_response(post, response_data)

    @patch('blog.api.controllers.post.JWTAuth.__call__')
    def test_post_retrieve_not_found(self, authenticate_mock):
        authenticate_mock.side_effect = mock_jwt_auth
        mommy.make('Post', id=2, _fill_optional=True)
        response = self.client.get('/api/posts/1', content_type='application/json')
        self.assertEquals(response.status_code, 404)

    @patch('blog.api.controllers.post.JWTAuth.__call__')
    def test_post_delete(self, authenticate_mock):
        authenticate_mock.side_effect = mock_jwt_auth
        post = mommy.make('Post', _fill_optional=True)
        response = self.client.delete(f'/api/posts/{post.id}', content_type='application/json')
        self.assertEquals(response.status_code, 204)
        self.assertEquals(Post.objects.count(), 0)

    @patch('blog.api.controllers.post.JWTAuth.__call__')
    def test_post_delete_not_found(self, authenticate_mock):
        authenticate_mock.side_effect = mock_jwt_auth
        mommy.make('Post', id=2, _fill_optional=True)
        response = self.client.delete('/api/posts/1', content_type='application/json')
        self.assertEquals(response.status_code, 404)
        self.assertEquals(Post.objects.count(), 1)
