import asyncio, os

from nats.aio.client import Client
from dotenv import load_dotenv
from handlers import CalculationWorkflowHandler
from utils import check_env_variables

load_dotenv()
check_env_variables("NATS_SERVER_URL", "OUTPUT_BASE_DIRECTORY")

server_url = os.getenv("NATS_SERVER_URL")


async def main():

    pub_topic = "topic.to.sort"
    sub_topic = "topic.to.calculate"

    client = Client()

    try:
        await client.connect(server_url)
        print("connected to the Nats server")
        cwh = CalculationWorkflowHandler(client, pub_topic)

        await client.subscribe(sub_topic, cb=cwh.message_handler)

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
