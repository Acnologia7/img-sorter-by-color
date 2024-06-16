import asyncio, nats, os, json

from nats.aio.client import Client
from nats.aio.msg import Msg

from img_process_functions import mean_color, convert_rgb_to_names


server_url = os.getenv("NATS_SERVER_URL")


async def message_handler(msg: Msg, client: Client) -> None:
    subject = msg.subject
    data = msg.data.decode()
    print(f"Received a message on '{subject}': {data}")

    image_path = data

    try:
        mean_rgb = await mean_color(image_path)
        color_name = await convert_rgb_to_names(mean_rgb)

        result = {
            "image_path": image_path,
            "mean_rgb": mean_rgb,
            "color_name": color_name,
        }

        json_data = json.dumps(result)
        result_message = json_data.encode()

        await client.publish("topic.to.sort", result_message)
        print(f"Published result to topic.to.sort {result}")

    except Exception as e:
        print(f"Error processing message: {e}")


async def main():

    try:
        client = await nats.connect(server_url)
        print("connected to the Nats server")

        async def handler(msg: Msg) -> None:
            await message_handler(msg, client)

        await client.subscribe("topic.to.calculate", cb=handler)
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
