import asyncio
import nats
import os

from PIL import Image
from dotenv import load_dotenv
from nats.aio.client import Client
from nats.aio.msg import Msg
from constants import IMAGE_FILE_EXTENSIONS


load_dotenv()

cache = set()
lock = asyncio.Lock()
inputs_path = os.getenv("INPUT_FOLDER")
scan_interval = int(os.getenv("SCAN_INTERVAL", 10))
server_url = os.getenv("NATS_SERVER_URL")


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

            if image_path in cache:
                continue

            if await is_verified(image_path):
                image_paths.append(image_path)
                async with lock:
                    cache.add(image_path)
                    print(f"Validated image: {image_path}")
            else:
                print(f"Image validation failed, it is not an image: {image_path}")

    except asyncio.TimeoutError:
        pass

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
    except Exception:
        return False


async def publish_messages(image_paths: str, client: Client) -> None:
    for image_path in image_paths:
        await client.publish("topic.to.calculate", image_path.encode())
        print(f"Sent image path to NATS: {image_path}")


async def message_handler(msg: Msg) -> None:
    subject = msg.subject
    reply = msg.reply
    data = msg.data.decode()
    print(
        "Received a message on '{subject} {reply}': {data}".format(
            subject=subject, reply=reply, data=data
        )
    )
    async with lock:
        cache.remove(data)


async def main():

    try:
        client = await nats.connect(server_url)
        print("connected to the Nats server")
        await client.subscribe("topic.to.invalidate", cb=message_handler)

        while True:
            image_paths = await scan_folder_for_images(inputs_path)
            if image_paths:
                await publish_messages(image_paths, client)
            await asyncio.sleep(scan_interval)

    except asyncio.CancelledError:
        pass

    except Exception as e:
        print(f"Error in main loop: {e}")

    finally:
        print("disconnecting...")
        await client.drain()
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
