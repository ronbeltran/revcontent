import unittest
import json
import responses

from revcontent.revcontent_client import Revcontent
from revcontent.revcontent_client import RevcontentException
from revcontent.revcontent_client import REVCONTENT_API


class RevcontentTestCase(unittest.TestCase):
    def setUp(self):
        self.client_id = 'abc'
        self.client_secret = 'secret'
        self.dummy_access_token = 'FOOBAR'
        self.dummy_access_token_body = {
            'token_type': 'Bearer',
            'access_token': self.dummy_access_token,
            'scope': 'advertiser publisher',
            'expires_in': 86400
        }

    @responses.activate
    def test_login_success(self):
        responses.add(
            responses.POST, REVCONTENT_API + '/oauth/token',
            content_type='application/json',
            json=self.dummy_access_token_body, status=200)

        revcontent = Revcontent(self.client_id, self.client_secret)
        revcontent.login()

        self.assertIsNotNone(revcontent.token)
        self.assertEqual(self.dummy_access_token, revcontent.token)

    @responses.activate
    def test_login_failure(self):
        body = {
            'error': 'invalid_client',
            'error_description': 'The client credentials are invalid',
        }

        responses.add(
            responses.POST, REVCONTENT_API + '/oauth/token',
            content_type='application/json',
            body=RevcontentException(400, json.dumps(body)), status=400)

        # get reference to the exception as `excp`
        with self.assertRaises(RevcontentException) as excp:
            revcontent = Revcontent(self.client_id, self.client_secret)
            revcontent.login()

        # assert exception contents
        excp_contents = excp.exception
        self.assertEqual(excp_contents.status_code, 400)
        self.assertEqual(excp_contents.text, json.dumps(body))

    @responses.activate
    def test_get_brand_targets_success(self):
        body = {
            'success': True,
            'data': [
                {'name': 'example.com', 'id': '1'},
                {'name': 'somewhere.com', 'id': '2'},
            ]
        }

        responses.add(
            responses.POST, REVCONTENT_API + '/oauth/token',
            content_type='application/json',
            json=self.dummy_access_token_body, status=200)

        responses.add(
            responses.GET, REVCONTENT_API + '/stats/api/v1.0/boosts/brands',
            content_type='application/json',
            json=body, status=200)

        revcontent = Revcontent(self.client_id, self.client_secret)
        revcontent.login()

        resp = revcontent.get_brand_targets()
        self.assertEqual(200, resp.status_code)

        r = resp.json()

        self.assertTrue(r['success'])
        self.assertEqual(2, len(r['data']))
        self.assertDictEqual(r, body)

    @responses.activate
    def test_get_brand_targets_failure(self):
        body = {
            'success': False,
            'errors': [
                {
                    "code": 100,
                    "title": "Invalid Argument",
                    "detail": "Invalid ID value"
                }
            ]
        }

        responses.add(
            responses.POST, REVCONTENT_API + '/oauth/token',
            content_type='application/json',
            json=self.dummy_access_token_body, status=200)

        responses.add(
            responses.GET, REVCONTENT_API + '/stats/api/v1.0/boosts/brands',
            content_type='application/json',
            json=body, status=409)

        revcontent = Revcontent(self.client_id, self.client_secret)
        revcontent.login()

        resp = revcontent.get_brand_targets()
        self.assertEqual(409, resp.status_code)

        r = resp.json()

        self.assertFalse(r['success'])
        self.assertIn('errors', r)
        self.assertDictEqual(r, body)

    @responses.activate
    def test_get_topic_targets_success(self):
        body = {
            'success': True,
            'data': [
                {'name': 'example.com', 'id': '1'},
                {'name': 'somewhere.com', 'id': '2'},
            ]
        }

        responses.add(
            responses.POST, REVCONTENT_API + '/oauth/token',
            content_type='application/json',
            json=self.dummy_access_token_body, status=200)

        responses.add(
            responses.GET, REVCONTENT_API + '/stats/api/v1.0/boosts/targets',
            content_type='application/json',
            json=body, status=200)

        revcontent = Revcontent(self.client_id, self.client_secret)
        revcontent.login()

        resp = revcontent.get_topic_targets()
        self.assertEqual(200, resp.status_code)

        r = resp.json()

        self.assertTrue(r['success'])
        self.assertEqual(2, len(r['data']))
        self.assertDictEqual(r, body)

    @responses.activate
    def test_get_topic_targets_failure(self):
        body = {
            'success': False,
            'errors': [
                {
                    "code": 100,
                    "title": "Invalid Argument",
                    "detail": "Invalid ID value"
                }
            ]
        }

        responses.add(
            responses.POST, REVCONTENT_API + '/oauth/token',
            content_type='application/json',
            json=self.dummy_access_token_body, status=200)

        responses.add(
            responses.GET, REVCONTENT_API + '/stats/api/v1.0/boosts/targets',
            content_type='application/json',
            json=body, status=409)

        revcontent = Revcontent(self.client_id, self.client_secret)
        revcontent.login()

        resp = revcontent.get_topic_targets()
        self.assertEqual(409, resp.status_code)

        r = resp.json()

        self.assertFalse(r['success'])
        self.assertIn('errors', r)
        self.assertDictEqual(r, body)

    @responses.activate
    def test_get_countries_success(self):
        body = {
            'success': True,
            'data': [
                {'id': 'ZA', 'name': 'South Africa'},
                {'id': 'ZM', 'name': 'Zambia'},
                {'id': 'ZW', 'name': 'Zimbabwe'},
            ]
        }

        responses.add(
            responses.POST, REVCONTENT_API + '/oauth/token',
            content_type='application/json',
            json=self.dummy_access_token_body, status=200)

        responses.add(
            responses.GET, REVCONTENT_API + '/stats/api/v1.0/countries',
            content_type='application/json',
            json=body, status=200)

        revcontent = Revcontent(self.client_id, self.client_secret)
        revcontent.login()

        resp = revcontent.get_countries()
        self.assertEqual(200, resp.status_code)

        r = resp.json()

        self.assertTrue(r['success'])
        self.assertEqual(3, len(r['data']))
        self.assertDictEqual(r, body)

    @responses.activate
    def test_get_countries_failure(self):
        body = {
            'errors': [
                {'code': 500, 'title': 'Server error.'},
            ]
        }

        responses.add(
            responses.POST, REVCONTENT_API + '/oauth/token',
            content_type='application/json',
            json=self.dummy_access_token_body, status=200)

        responses.add(
            responses.GET, REVCONTENT_API + '/stats/api/v1.0/countries',
            content_type='application/json',
            json=body, status=500)

        revcontent = Revcontent(self.client_id, self.client_secret)
        revcontent.login()

        resp = revcontent.get_countries()
        self.assertEqual(500, resp.status_code)

        r = resp.json()

        self.assertIn('errors', r)
        self.assertEqual(1, len(r['errors']))
        self.assertDictEqual(r, body)

    @responses.activate
    def test_get_devices_success(self):
        body = {
            'success': True,
            'data': [
                {'name': 'desktop', 'id': '1'},
                {'name': 'mobile', 'id': '2'},
                {'name': 'tablet', 'id': '3'},
                {'name': 'android', 'id': '4'},
                {'name': 'ios', 'id': '5'},
                {'name': 'windows', 'id': '6'},
            ]
        }

        responses.add(
            responses.POST, REVCONTENT_API + '/oauth/token',
            content_type='application/json',
            json=self.dummy_access_token_body, status=200)

        responses.add(
            responses.GET, REVCONTENT_API + '/stats/api/v1.0/devices',
            content_type='application/json',
            json=body, status=200)

        revcontent = Revcontent(self.client_id, self.client_secret)
        revcontent.login()

        resp = revcontent.get_devices()
        self.assertEqual(200, resp.status_code)

        r = resp.json()

        self.assertTrue(r['success'])
        self.assertEqual(6, len(r['data']))
        self.assertDictEqual(r, body)

    @responses.activate
    def test_get_devices_failure(self):
        body = {
            'errors': [
                {'code': 500, 'title': 'Server error.'},
            ]
        }

        responses.add(
            responses.POST, REVCONTENT_API + '/oauth/token',
            content_type='application/json',
            json=self.dummy_access_token_body, status=200)

        responses.add(
            responses.GET, REVCONTENT_API + '/stats/api/v1.0/devices',
            content_type='application/json',
            json=body, status=500)

        revcontent = Revcontent(self.client_id, self.client_secret)
        revcontent.login()

        resp = revcontent.get_devices()
        self.assertEqual(500, resp.status_code)

        r = resp.json()

        self.assertIn('errors', r)
        self.assertEqual(1, len(r['errors']))
        self.assertDictEqual(r, body)

    @responses.activate
    def test_get_languages_success(self):
        body = {
            'success': True,
            'data': [
                {'name': 'english', 'id': '1'},
                {'name': 'spanish', 'id': '2'},
                {'name': 'chinese', 'id': '3'},
                {'name': 'german', 'id': '4'},
                {'name': 'french', 'id': '5'},
                {'name': 'hindi', 'id': '6'},
                {'name': 'arabic', 'id': '7'},
                {'name': 'portuguese', 'id': '8'},
                {'name': 'russian', 'id': '9'},
                {'name': 'bengali', 'id': '10'},
                {'name': 'japanese', 'id': '11'},
                {'name': 'dutch', 'id': '12'},
                {'name': 'italian', 'id': '13'},
                {'name': 'swedish', 'id': '14'},
                {'name': 'danish', 'id': '15'},
                {'name': 'malay', 'id': '16'},
                {'name': 'romanian', 'id': '17'},
                {'name': 'indonesian', 'id': '18'},
                {'name': 'slovak', 'id': '19'},
                {'name': 'bulgarian', 'id': '20'},
                {'name': 'hebrew', 'id': '21'}
            ]
        }

        responses.add(
            responses.POST, REVCONTENT_API + '/oauth/token',
            content_type='application/json',
            json=self.dummy_access_token_body, status=200)

        responses.add(
            responses.GET, REVCONTENT_API + '/stats/api/v1.0/languages',
            content_type='application/json',
            json=body, status=200)

        revcontent = Revcontent(self.client_id, self.client_secret)
        revcontent.login()

        resp = revcontent.get_languages()
        self.assertEqual(200, resp.status_code)

        r = resp.json()

        self.assertTrue(r['success'])
        self.assertEqual(21, len(r['data']))
        self.assertDictEqual(r, body)

    @responses.activate
    def test_get_languages_failure(self):
        body = {
            'errors': [
                {'code': 500, 'title': 'Server error.'},
            ]
        }

        responses.add(
            responses.POST, REVCONTENT_API + '/oauth/token',
            content_type='application/json',
            json=self.dummy_access_token_body, status=200)

        responses.add(
            responses.GET, REVCONTENT_API + '/stats/api/v1.0/languages',
            content_type='application/json',
            json=body, status=500)

        revcontent = Revcontent(self.client_id, self.client_secret)
        revcontent.login()

        resp = revcontent.get_languages()
        self.assertEqual(500, resp.status_code)

        r = resp.json()

        self.assertIn('errors', r)
        self.assertEqual(1, len(r['errors']))
        self.assertDictEqual(r, body)

    @responses.activate
    def test_get_interests_success(self):
        body = {
            'success': True,
            'data': [
                {'id': '2855', 'people': '196', 'CPW': '9', 'parent_id': '2573', 'name': 'Paintball Fields', 'targetable': 'false'},  # noqa
                {'id': '1767', 'people': '6', 'CPW': '0', 'parent_id': '1765', 'name': 'Linguistics Conferences', 'targetable': 'true'},  # noqa
                {'id': '2290', 'people': '51', 'CPW': '0', 'parent_id': '2868', 'name': 'Internet Encyclopedia of Philosophy', 'targetable': 'true'}  # noqa
            ]
        }

        responses.add(
            responses.POST, REVCONTENT_API + '/oauth/token',
            content_type='application/json',
            json=self.dummy_access_token_body, status=200)

        responses.add(
            responses.GET, REVCONTENT_API + '/stats/api/v1.0/interests',
            content_type='application/json',
            json=body, status=200)

        revcontent = Revcontent(self.client_id, self.client_secret)
        revcontent.login()

        resp = revcontent.get_interests()
        self.assertEqual(200, resp.status_code)

        r = resp.json()

        self.assertTrue(r['success'])
        self.assertEqual(3, len(r['data']))
        self.assertDictEqual(r, body)

    @responses.activate
    def test_get_interests_failure(self):
        body = {
            'errors': [
                {'code': 500, 'title': 'Server error.'},
            ]
        }

        responses.add(
            responses.POST, REVCONTENT_API + '/oauth/token',
            content_type='application/json',
            json=self.dummy_access_token_body, status=200)

        responses.add(
            responses.GET, REVCONTENT_API + '/stats/api/v1.0/interests',
            content_type='application/json',
            json=body, status=500)

        revcontent = Revcontent(self.client_id, self.client_secret)
        revcontent.login()

        resp = revcontent.get_interests()
        self.assertEqual(500, resp.status_code)

        r = resp.json()

        self.assertIn('errors', r)
        self.assertEqual(1, len(r['errors']))
        self.assertDictEqual(r, body)
