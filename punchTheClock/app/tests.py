from datetime import datetime
from django.test import TestCase
from django.test import Client

from django.contrib.auth.models import User
from django.utils import timezone

from .models import TimeLog

TEST_USER_NAME = 'testuser'
TEST_USER_PWD = '12345'


def addUser():
    user = User.objects.create(username=TEST_USER_NAME)
    user.set_password(TEST_USER_PWD)
    user.save()
    return user


def addTimeLog(user):
    tl = TimeLog.objects.create(start_date=timezone.now(),
                                end_date=timezone.now(),
                                user_id=user)
    tl.save()
    return tl


class APITests(TestCase):
    def test_get_not_allowed(self):
        client = Client()
        response = client.get('/api/punch')
        self.assertEqual(response.status_code, 405)

    def test_put_not_allowed(self):
        client = Client()
        response = client.put('/api/punch')
        self.assertEqual(response.status_code, 405)

    def test_no_token(self):
        client = Client()
        response = client.post('/api/punch')
        self.assertEqual(response.status_code, 403)

    def test_invalid_token(self):
        client = Client()
        response = client.post('/api/punch', HTTP_AUTHORIZATION='fooBar')
        self.assertEqual(response.status_code, 403)

    def test_token_creation(self):
        addUser()
        client = Client()
        client.login(username='testuser', password='12345')
        response = client.post('/token')
        self.assertEqual(response.status_code, 200)

    def test_api_punch(self):
        addUser()
        client = Client()
        client.login(username='testuser', password='12345')
        response = client.post('/token')
        self.assertEqual(response.status_code, 200)
        client.logout()

        token = response.context[2]['widget']['value']

        # TimeLog is created with 'null' as end time
        response = client.post('/api/punch', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertContains(response, 'created')
        self.assertContains(response, 'null')

        # TimeLog is updated and no 'null' remains
        response = client.post('/api/punch', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertContains(response, 'updated')
        self.assertNotContains(response, 'null')

    def test_timelog_removal(self):
        user = addUser()
        client = Client()
        client.login(username='testuser', password='12345')

        for i in range(0, 10):
            addTimeLog(user)

        response = client.get('/list')
        self.assertEqual(response.status_code, 200)
        search_phrase = datetime.now().strftime('%d.%m.%Y</td>')
        self.assertEqual(response.content.decode().count(search_phrase), 10)

        response = client.post('/details/1', {'delete': ''})
        response = client.get('/list')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode().count(search_phrase), 9)

    def test_timelog_update(self):
        user = addUser()
        client = Client()
        client.login(username='testuser', password='12345')
        addTimeLog(user)

        newDateTime = timezone.datetime(2020, 10, 31, 11, 11)
        response = client.post('/details/1',
                               {
                                   'update': '',
                                   'start_date': newDateTime,
                                   'end_date': newDateTime
                               })
        self.assertEqual(response.status_code, 200)

        response = client.get('/details/1')
        self.assertEqual(response.content.decode().count('2020-10-31 11:11:00'), 2)
