"""
Test chaos class
"""
from .conftest import mock_open_ai_response_object


def test_chaos(mocker, chaos):
    # Mock function and method that requests openai API (to avoid costs)
    mocker.patch(
        "auto_chaos.chaos.generate_text",
        return_value=mock_open_ai_response_object(
            mocker=mocker, content="TEST_ACTION, TEST_ACTION, TEST_ACTION"
        ),
    )

    chaos.chaos(objective=10)
    assert len(chaos.systems[0].results) == 3
    assert len(chaos.messages) == 24
    chaos.report()
    assert len(chaos.messages) == 25
