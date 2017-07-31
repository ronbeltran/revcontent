import logging
import requests

logger = logging.getLogger(__name__)

REVCONTENT_API = 'https://api.revcontent.io'


class RevcontentException(Exception):
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text

    def __str__(self):
        return '{0}:  {1}'.format(self.status_code, self.text)


class Revcontent(object):
    def __init__(self, client_id, client_secret, grant_type='client_credentials'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.grant_type = grant_type
        self.token = None
        self.headers = {
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache',
        }

    def fetch(self, method, url, **kwargs):
        """
        TODO: Handle expired access token, re-login on expire
        """
        HTTP_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS', 'HEAD']
        method = method.strip().upper()

        if method.strip().upper() not in HTTP_METHODS:
            raise ValueError('Invalid Http Method: {}'.format(method))

        return requests.request(method, url, **kwargs)

    def login(self):
        """ POST https://api.revcontent.io/oauth/token """
        if self.token is None:
            self.headers['Content-Type'] = 'application/x-www-form-urlencode'
            payload = {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'grant_type': self.grant_type,
            }
            resp = self.fetch('POST', REVCONTENT_API + '/oauth/token', data=payload)
            if resp.status_code == 200:
                data = resp.json()
                self.token = data['access_token']
                self.headers.update({
                    'Authorization': 'Bearer {}'.format(self.token),
                    'Content-Type': 'application/json',
                })
            else:
                logger.error('Failed to get Revcontent access token.')
                raise RevcontentException(resp.status_code, resp.text)

    def get_brand_targets(self):
        """ GET https://api.revcontent.io/stats/api/v1.0/boosts/brands """
        return self.fetch('GET', REVCONTENT_API + '/stats/api/v1.0/boosts/brands',
                          headers=self.headers)

    def get_topic_targets(self):
        """ GET https://api.revcontent.io/stats/api/v1.0/boosts/targets """
        return self.fetch('GET', REVCONTENT_API + '/stats/api/v1.0/boosts/targets',
                          headers=self.headers)

    def get_countries(self):
        """ GET https://api.revcontent.io/stats/api/v1.0/countries """
        return self.fetch('GET', REVCONTENT_API + '/stats/api/v1.0/countries',
                          headers=self.headers)

    def get_devices(self):
        """ GET https://api.revcontent.io/stats/api/v1.0/devices """
        return self.fetch('GET', REVCONTENT_API + '/stats/api/v1.0/devices',
                          headers=self.headers)

    def get_languages(self):
        """ GET https://api.revcontent.io/stats/api/v1.0/languages """
        return self.fetch('GET', REVCONTENT_API + '/stats/api/v1.0/languages',
                          headers=self.headers)

    def get_interests(self):
        """ GET https://api.revcontent.io/stats/api/v1.0/interests """
        return self.fetch('GET', REVCONTENT_API + '/stats/api/v1.0/interests',
                          headers=self.headers)
