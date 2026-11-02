from unittest.mock import Mock

import pytest
import requests

from api_client import fetch_todo

URL = "https://example.com/todo/1"


def test_fetch_todo_success(monkeypatch):
    payload = {
        "userId": 1,
        "id": 1,
        "title": "test todo",
        "completed": False,
    }
    response = Mock()
    response.json.return_value = payload

    mock_get = Mock(return_value=response)
    monkeypatch.setattr(requests, "get", mock_get)

    result = fetch_todo(URL)

    assert result == payload
    mock_get.assert_called_once_with(URL, timeout=5.0)
    response.raise_for_status.assert_called_once_with()


def test_fetch_todo_timeout(monkeypatch):
    monkeypatch.setattr(
        requests,
        "get",
        Mock(side_effect=requests.exceptions.Timeout("request timed out")),
    )

    with pytest.raises(requests.exceptions.Timeout):
        fetch_todo(URL)


def test_fetch_todo_http_error(monkeypatch):
    response = Mock()
    response.raise_for_status.side_effect = requests.exceptions.HTTPError("500 error")
    monkeypatch.setattr(requests, "get", Mock(return_value=response))

    with pytest.raises(requests.exceptions.HTTPError):
        fetch_todo(URL)

    response.raise_for_status.assert_called_once_with()


def test_fetch_todo_request_error(monkeypatch):
    monkeypatch.setattr(
        requests,
        "get",
        Mock(side_effect=requests.exceptions.ConnectionError("connection failed")),
    )

    with pytest.raises(requests.exceptions.RequestException):
        fetch_todo(URL)
