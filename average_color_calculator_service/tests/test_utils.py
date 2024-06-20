import pytest, json

from unittest.mock import AsyncMock, patch, MagicMock
from PIL import UnidentifiedImageError
from nats.aio.client import Client

from src.utils import *


@pytest.mark.asyncio
async def test_is_verified_nonexistent_file():
    with patch("os.path.exists", return_value=False):
        result = await is_verified("nonexistent_file.jpg")
        assert result == False


@pytest.mark.asyncio
async def test_is_verified_valid_image():
    with patch("os.path.exists", return_value=True):
        mock_img = MagicMock()

        with patch("PIL.Image.open", return_value=mock_img):
            result = await is_verified("valid_image.jpg")
            assert result == True


@pytest.mark.asyncio
async def test_is_verified_invalid_image():
    with patch("os.path.exists", return_value=True):
        with patch("PIL.Image.open", side_effect=UnidentifiedImageError):
            result = await is_verified("invalid_image.jpg")
            assert result == False


@pytest.mark.asyncio
async def test_is_verified_with_general_exception():
    with patch("os.path.exists", return_value=True):
        with patch("PIL.Image.open", side_effect=Exception("General error")):
            result = await is_verified("general_error_image.jpg")
            assert result == False


@pytest.mark.asyncio
async def test_publish_message_success():
    nc = Client()
    msg = json.dumps({"key": "value"})
    pub_topic = "test/topic"
    nc.publish = AsyncMock()

    await publish_message(msg, nc, pub_topic)

    expected_encoded_msg = msg.encode()
    nc.publish.assert_called_once_with(pub_topic, expected_encoded_msg)


@pytest.mark.asyncio
async def test_publish_message_exception():
    nc = Client()
    msg = json.dumps({"key": "value"})
    pub_topic = "test/topic"
    nc.publish = AsyncMock()
    nc.publish.side_effect = Exception("Test exception")

    with patch("builtins.print") as mocked_print:
        await publish_message(msg, nc, pub_topic)
        mocked_print.assert_called_with(
            f"Error with publishing message on {pub_topic}: {msg.encode()} Test exception"
        )


def test_build_json_message_with_mean_rgb():
    file_path = "path/to/file.jpg"
    mean_rgb = [123, 234, 45]
    expected_output = json.dumps(
        {
            "file_path": file_path,
            "mean_rgb": mean_rgb,
            "color_name": None,
            "is_ui_request": False,
        }
    )
    result = build_json_message(file_path, mean_rgb=mean_rgb)
    assert result == expected_output


def test_build_json_message_with_color_name():
    file_path = "path/to/file.jpg"
    color_name = "red"
    expected_output = json.dumps(
        {
            "file_path": file_path,
            "mean_rgb": None,
            "color_name": color_name,
            "is_ui_request": False,
        }
    )
    result = build_json_message(file_path, color_name=color_name)
    assert result == expected_output


def test_build_json_message_with_is_ui_request():
    file_path = "path/to/file.jpg"
    is_ui_request = True
    expected_output = json.dumps(
        {
            "file_path": file_path,
            "mean_rgb": None,
            "color_name": None,
            "is_ui_request": is_ui_request,
        }
    )
    result = build_json_message(file_path, is_ui_request=is_ui_request)
    assert result == expected_output


def test_build_json_message_all_values():
    file_path = "path/to/file.jpg"
    mean_rgb = [123, 234, 45]
    color_name = "red"
    is_ui_request = True
    expected_output = json.dumps(
        {
            "file_path": file_path,
            "mean_rgb": mean_rgb,
            "color_name": color_name,
            "is_ui_request": is_ui_request,
        }
    )
    result = build_json_message(
        file_path, mean_rgb=mean_rgb, color_name=color_name, is_ui_request=is_ui_request
    )
    assert result == expected_output
