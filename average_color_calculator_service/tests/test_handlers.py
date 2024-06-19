import pytest, json
from unittest.mock import AsyncMock, MagicMock, patch
from nats.aio.client import Client, Msg
from src.handlers import BaseHandler


@pytest.fixture
def mock_msg():
    msg = MagicMock(Msg)
    msg.data = json.dumps({"key": "value"}).encode()
    return msg


@pytest.mark.asyncio
async def test_call_message_base_handler_success(mock_msg):
    nc = Client()
    handler = BaseHandler(nc, "test_topic")
    handler.process_message = AsyncMock()

    await handler.message_handler(mock_msg)
    handler.process_message.assert_called_once_with({"key": "value"})


@pytest.mark.asyncio
async def test_call_message_base_handler_exception(mock_msg):
    nc = Client()
    handler = BaseHandler(nc, "test_topic")
    handler.process_message = AsyncMock(side_effect=Exception("Test Exception"))

    await handler.message_handler(mock_msg)
    handler.process_message.assert_called_once_with({"key": "value"})

    with patch("builtins.print") as mocked_print:
        await handler.message_handler(mock_msg)
        mocked_print.assert_called_with("Error in message handling: Test Exception")


@pytest.mark.asyncio
async def test_call_base_handler_publish_message():
    nc = Client()
    handler = BaseHandler(nc, "test_topic")
    test_msg = json.dumps({"key": "value"})
    nc.publish = AsyncMock()

    await handler.publish_message(test_msg)
    nc.publish.assert_called_once_with("test_topic", test_msg.encode())
