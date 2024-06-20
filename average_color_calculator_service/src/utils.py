import json, os

from PIL import Image
from nats.aio.client import Client
import pytest


async def is_verified(image_path: str) -> bool:
    if not os.path.exists(image_path):
        return False

    try:
        with Image.open(image_path) as img:
            img.verify()
        return True
    except Exception as e:
        print("Error with img verification", e)
        return False


async def publish_message(msg: dict, client: Client, pub_topic: str) -> None:
    try:
        encoded_msg = msg.encode()
        await client.publish(pub_topic, encoded_msg)
        print(f"Sent message on '{pub_topic}': {encoded_msg}")
    except Exception as e:
        print(
            f"Error with publishing message on {pub_topic}: {encoded_msg} {e}",
        )


def check_env_variables(*vars):
    missing_vars = [var for var in vars if os.getenv(var) is None]
    if missing_vars:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing_vars)}"
        )


def build_json_message(
    file_path: str,
    mean_rgb: list = None,
    color_name: str = None,
    is_ui_request: bool = False,
) -> str:
    raw = {
        "file_path": file_path,
        "mean_rgb": mean_rgb,
        "color_name": color_name,
        "is_ui_request": is_ui_request,
    }
    json_msg = json.dumps(raw)
    return json_msg


def test_check_env_variables_all_present(monkeypatch):
    monkeypatch.setenv("INPUT_BASE_DIRECTORY", "/some/path")
    monkeypatch.setenv("SCAN_INTERVAL", "1")
    monkeypatch.setenv("NATS_SERVER_URL", "nats://test-case:0000")

    check_env_variables("INPUT_BASE_DIRECTORY", "SCAN_INTERVAL", "NATS_SERVER_URL")


def test_check_env_variables_missing(monkeypatch):
    monkeypatch.delenv("INPUT_BASE_DIRECTORY", raising=False)
    monkeypatch.delenv("SCAN_INTERVAL", raising=False)
    monkeypatch.delenv("NATS_SERVER_URL", raising=False)

    with pytest.raises(EnvironmentError) as excinfo:
        check_env_variables("INPUT_BASE_DIRECTORY", "SCAN_INTERVAL", "NATS_SERVER_URL")

    assert "Missing required environment variables" in str(excinfo.value)
    assert "INPUT_BASE_DIRECTORY" in str(excinfo.value)
    assert "SCAN_INTERVAL" in str(excinfo.value)
    assert "NATS_SERVER_URL" in str(excinfo.value)


def test_check_env_variables_partial_present(monkeypatch):
    monkeypatch.setenv("INPUT_BASE_DIRECTORY", "/some/path")
    monkeypatch.delenv("SCAN_INTERVAL", raising=False)
    monkeypatch.delenv("NATS_SERVER_URL", raising=False)

    with pytest.raises(EnvironmentError) as excinfo:
        check_env_variables("INPUT_BASE_DIRECTORY", "SCAN_INTERVAL", "NATS_SERVER_URL")

    assert "Missing required environment variables" in str(excinfo.value)
    assert "SCAN_INTERVAL" in str(excinfo.value)
    assert "NATS_SERVER_URL" in str(excinfo.value)
