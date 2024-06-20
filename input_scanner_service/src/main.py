import asyncio, os

from dotenv import load_dotenv
from nats.aio.client import Client

from utils import *
from handlers import UIWorkflowHandler


load_dotenv()
check_env_variables("INPUT_BASE_DIRECTORY", "SCAN_INTERVAL", "NATS_SERVER_URL")

inputs_path = os.getenv("INPUT_BASE_DIRECTORY")
scan_interval = int(os.getenv("SCAN_INTERVAL"))
server_url = os.getenv("NATS_SERVER_URL")


async def main():

    sub_topic = "topic.from.ui"
    pub_topic = "topic.to.calculate"

    client = Client()

    try:
        await build_input_point(inputs_path)
        await client.connect(server_url)
        print("connected to the Nats server")
        uiwh = UIWorkflowHandler(client, pub_topic)

        await client.subscribe(sub_topic, cb=uiwh.message_handler)

        while True:
            image_paths = await scan_folder_for_images(inputs_path)
            for image_path in image_paths:
                json_msg = build_json_message(file_path=image_path)
                await publish_message(json_msg, client, pub_topic)
                await asyncio.sleep(1)
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
