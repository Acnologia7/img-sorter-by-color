import asyncio, nats, os, json, shutil

from dotenv import load_dotenv
from nats.aio.client import Client
from nats.aio.msg import Msg

load_dotenv()

server_url = os.getenv("NATS_SERVER_URL")
sorted_base_url = os.getenv("OUTPUT_FOLDER")


async def message_handler(msg: Msg, client: Client) -> None:
    subject = msg.subject
    data = msg.data.decode()
    # print(f"Received a message on '{subject}': {data}")

    try:
        content = json.loads(data)
        source_path = content["image_path"]
        mean_rgb = content["mean_rgb"]
        color_name = content["color_name"]
        dest_path = f"{sorted_base_url}\{color_name}\{os.path.basename(source_path)}"
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        shutil.copy(source_path, dest_path)
        os.remove(source_path)

        await client.publish("topic.to.invalidate", str(source_path).encode())
        print(f"Published result to topic.to.invalidate")

    except Exception as e:
        print(f"Error processing message: {e}")


async def main():

    try:
        client = await nats.connect(server_url)
        print("connected to the Nats server")

        async def handler(msg: Msg) -> None:
            await message_handler(msg, client)

        await client.subscribe("topic.to.sort", cb=handler)
        while True:
            await asyncio.sleep(1)

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
