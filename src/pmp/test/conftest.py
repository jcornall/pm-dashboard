import pytest
from src.pmp.constants import PMP_API_URL
from src.pmp.test.mock_allpatches_response import __MOCK_ALLPATCHES_RESPONSES
from src.pmp.test.mock_allsystems_response import __MOCK_ALLSYSTEMS_RESPONSES


@pytest.fixture
def mock_pmp_api(requests_mock):
    requests_mock.post(
        "https://accounts.zoho.eu/oauth/v2/token",
        json={"access_token": "fake-access-token"},
    )
    requests_mock.get(
        f"{PMP_API_URL}/api/1.4/patch/allpatches", json=__return_allpatches_page
    )
    requests_mock.get(
        f"{PMP_API_URL}/api/1.4/patch/allsystems", json=__return_allsystems_page
    )


def __return_allpatches_page(req, ctx):
    return __MOCK_ALLPATCHES_RESPONSES[int(req.qs["page"][0]) - 1]


def __return_allsystems_page(req, ctx):
    return __MOCK_ALLSYSTEMS_RESPONSES[int(req.qs["page"][0]) - 1]
