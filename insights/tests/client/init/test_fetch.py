from insights.client import InsightsClient
from insights.client.config import InsightsConfig
from mock.mock import Mock
from pytest import fixture
from tempfile import NamedTemporaryFile


@fixture
def insights_client():
    config = InsightsConfig(http_timeout=123)
    client = InsightsClient(config)
    client.connection = Mock(base_url="http://www.example.com/")
    client.connection.get.return_value.headers.items.return_value = []
    return client


def test_request_with_etag(insights_client):
    """
    An egg fetch request with Etag is issued with correct timeout set.
    """
    etag_file = NamedTemporaryFile('w+t')
    etag_value = 'some_etag'
    etag_file.write(etag_value)
    etag_file.seek(0)

    source_path = 'some-source-path'
    insights_client._fetch(source_path, etag_file.name, "", force=False)

    url = "{0}{1}".format(insights_client.connection.base_url, source_path)
    headers = {'If-None-Match': etag_value}
    insights_client.connection.get.assert_called_once_with(url, headers=headers)


def test_request_forced(insights_client):
    """
    A forced egg fetch request is issued with correct timeout set.
    """
    source_path = 'some-source-path'
    insights_client._fetch(source_path, "", "", force=False)

    url = "{0}{1}".format(insights_client.connection.base_url, source_path)
    insights_client.connection.get.assert_called_once_with(url)
