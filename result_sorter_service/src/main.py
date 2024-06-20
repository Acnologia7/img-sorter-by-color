import asyncio, nats, os

from dotenv import load_dotenv

from handlers import SortWorkflowHandler
from utils import check_env_variables


load_dotenv()

check_env_variables("NATS_SERVER_URL", "OUTPUT_BASE_DIRECTORY")

server_url = os.getenv("NATS_SERVER_URL")


async def main():

    pub_topic = "topic.to.ui"
    sub_topic = "topic.to.sort"

    try:
        client = await nats.connect(server_url)
        print("connected to the Nats server")

        swh = SortWorkflowHandler(client, pub_topic)

        await client.subscribe(sub_topic, cb=swh.message_handler)
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
