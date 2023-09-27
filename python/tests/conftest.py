"""
Conftest
"""
import pytest

from auto_chaos.chaos import BaseSystem, Chaos


def mock_open_ai_response_object(mocker, content: str):
    """
    Mocks the response object from the openai api.
    """
    mock_generator_object = mocker.MagicMock()
    mock_message_object = mocker.MagicMock()
    mock_message_object.configure_mock(**{"message.content": content})
    mock_generator_object.configure_mock(**{"choices": [mock_message_object]})
    return mock_generator_object


class BaseSystemTest(BaseSystem):
    def test_action(self, args: list[str] = None):
        self.results.append("Tests")


@pytest.fixture
def chaos():
    system = BaseSystemTest()

    initial_state = {
        "system_resources": {},
        "api_routes": ["test", "test"],
        "availability_route": "test",
    }

    yield Chaos([system], initial_state)
