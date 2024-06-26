import os, json

from PIL import Image
from nats.aio.client import Client

try:
    from .constants import IMAGE_FILE_EXTENSIONS
except ImportError:
    from constants import IMAGE_FILE_EXTENSIONS


async def build_input_point(folder_path: str) -> None:
    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path, exist_ok=True)
            print(f"Subdirectory path {folder_path} successfuly built")

    except OSError as e:
        print(f"Error during building a subdirectory path {folder_path} {e}")


async def scan_folder_for_images(folder_path: str) -> list[str]:

    image_paths = []

    try:
        image_files = [
            f
            for f in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, f))
            and f.lower().endswith(IMAGE_FILE_EXTENSIONS)
        ]

        for image_file in image_files:
            image_path = os.path.join(folder_path, image_file)

            if await is_verified(image_path):
                image_paths.append(image_path)
                print(f"Validated image: {image_path}")
            else:
                print(f"Image validation failed, it is not an image: {image_path}")

    except Exception as e:
        print(f"Error during folder scanning: {e}")

    return image_paths


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


async def publish_message(msg: str, client: Client, pub_topic: str) -> None:

    encoded_msg = msg.encode()

    try:
        await client.publish(pub_topic, encoded_msg)
        print(f"Sent message on {pub_topic}: {encoded_msg}")
    except Exception as e:
        print(f"Error with publishing message on {pub_topic}: {encoded_msg} {e}")


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
