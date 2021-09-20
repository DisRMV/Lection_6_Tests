import pytest
import requests
import os


class TestYandexAPIPytest:

    @classmethod
    def setup_class(cls):
        cls.token = os.environ.get('YA_TOKEN')
        cls.url = 'https://cloud-api.yandex.net/v1/disk/resources'
        cls.headers = {'Authorization': f'OAuth {cls.token}'}
        cls.response = requests.put(cls.url, headers=cls.headers, params={'path': 'test_catalog'})
        cls.response_existence = requests.get(cls.url, headers=cls.headers, params={'path': 'test_catalog'})

    @classmethod
    def teardown_class(cls):
        requests.delete(cls.url, headers=cls.headers, params={'path': 'test_catalog', 'permanently': 'true'})

    def test_catalog_created(self):
        assert self.response.status_code == 201
        assert self.response_existence.status_code == 200

    @pytest.mark.xfail
    @pytest.mark.parametrize('status_code', [400, 401, 403, 404, 406, 409, 423, 429, 503, 507])
    def test_catalog_not_created(self, status_code):
        if self.response.status_code == 201:
            pytest.skip('Папка создана успешно. Отрицательный тест пропущен')
        assert self.response.status_code == status_code
