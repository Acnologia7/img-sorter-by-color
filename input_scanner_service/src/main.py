import nats, asyncio, os
from dotenv import load_dotenv

try:
    from .utils import *
    from .handlers import UIWorkflowHandler
except ImportError:
    from utils import *
    from handlers import UIWorkflowHandler

load_dotenv()

inputs_path = os.getenv("INPUT_BASE_DIRECTORY")
scan_interval = int(os.getenv("SCAN_INTERVAL", 2))
server_url = os.getenv("NATS_SERVER_URL")


async def main():

    sub_topic = "topic.from.ui"
    pub_topic = "topic.to.calculate"

    client = await nats.connect(server_url)

    try:
        print("connected to the Nats server")
        uiwh = UIWorkflowHandler(client, pub_topic)

        await client.subscribe(sub_topic, cb=uiwh.message_handler)

        while True:
            image_paths = await scan_folder_for_images(inputs_path)
            for image_path in image_paths:
                json_msg = build_json_message(file_path=image_path)
                await publish_message(json_msg, client, pub_topic)
                await asyncio.sleep(2)
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
