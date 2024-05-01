import pytest
from unittest.mock import patch, MagicMock
from tasks import collect_links, parse_xml_form
from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379', backend='redis://localhost:6379')


app.conf.update(
    task_always_eager=True,
)
@pytest.fixture
def mocked_requests_get():
    mock_get = MagicMock()

    response_mock = MagicMock()
    response_mock.status_code = 200
    response_mock.text = ''

    mock_get.return_value = response_mock

    with patch('requests.get', mock_get):
        yield mock_get


def test_collect_links(mocked_requests_get):
    page_url = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?fz44=on&pageNumber=1'
    response_text = '<a href="/view.html?regNumber=1234">Link</a>'
    mocked_requests_get.return_value.text = response_text

    result = collect_links(page_url)

    assert len(result) == 1
    assert result[0] == 'https://zakupki.gov.ru/viewXml.html?regNumber=1234'


def test_parse_xml_form(mocked_requests_get):
    xml_link = 'https://zakupki.gov.ru/epz/order/notice/printForm/viewXml.html?regNumber=1234'
    response_text = '<publishDTInEIS>2023-10-15</publishDTInEIS>'
    mocked_requests_get.return_value.text = response_text

    result = parse_xml_form(xml_link)

    assert result == f'{xml_link} - 2023-10-15'