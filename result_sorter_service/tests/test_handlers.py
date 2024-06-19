import os
import shutil
import pytest, json
from unittest.mock import AsyncMock, MagicMock, patch
from nats.aio.client import Client, Msg
from src.handlers import BaseHandler, SortWorkflowHandler


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


@pytest.fixture
def setup_test_data():

    test_dir = "test_images"
    os.makedirs(test_dir, exist_ok=True)

    image_path = os.path.join(test_dir, "test_image.png")
    open(image_path, "a").close()

    yield image_path

    shutil.rmtree(test_dir)


@pytest.mark.asyncio
async def test_sort_img(setup_test_data):
    assert os.environ["OUTPUT_BASE_DIRECTORY"] == "/output"
    # output_base_directory = "/output" if os.name == "posix" else "\\output"

    image_path = setup_test_data
    color_name = "red"
    assert os.path.exists(image_path)
    nc = Client()
    pub_topic = "test_topic"
    handler = SortWorkflowHandler(nc, pub_topic)

    result = await handler.sort_img(image_path, color_name)

    assert os.path.exists(result)
    assert not os.path.exists(image_path)
