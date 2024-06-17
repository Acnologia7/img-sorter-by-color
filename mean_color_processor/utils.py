import json, os
from PIL import Image
from nats.aio.client import Client


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


async def publish_message(msg: dict, client: Client, pub_topic: str) -> None:
    try:
        encoded_msg = msg.encode()
        await client.publish(pub_topic, encoded_msg)
        print(f"Sent message on '{pub_topic}': {encoded_msg}")
    except Exception as e:
        print(f"Error with publishing message on'{pub_topic}': {encoded_msg}", e)
